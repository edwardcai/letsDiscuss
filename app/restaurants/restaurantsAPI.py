import httplib
import urllib2
import json
import requests
import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import app.restaurants.yelpAPI as yelpAPI
from app.restaurants.lda.ldaModel import *
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


class RestaurantsAPI(object):
	def __init__(self):
		self._url = "https://developers.zomato.com/api/v2.1"
		self._restaurant=None
		self._ldaModel = LdaModel()
		self._reviews = None
		with open('app/restaurants/config_zomato.json') as config_file:
			data = json.load(config_file)
		self._api_key = data["api-key"]
		self._headers = {"Accept": "application/json", "user-key": self._api_key}



	def getYelpClient(self):
		#load yelp API
		with open('app/restaurants/config_yelp.json') as cred:
		    creds = json.load(cred)
		    auth = Oauth1Authenticator(**creds)
		    return Client(auth)

	def discuss(self, query = None):
		if query == None:
			topic = self._ldaModel.getRecommendedTopic()
		else:
			"""Given a query, classifies the query according to LDA, and returns
			a review snippet of the same topic"""
			topic = self._ldaModel.getTopTopic(query)

		recommendation = self._ldaModel.generateRecommendedTopic()
		response = (str(self._ldaModel.getTopReview(topic)) + "... " + 
			"Would you like to hear my opinion on " + str(recommendation) + "?")
		return (response, self._ldaModel.idToTopic(topic))


	def search(self, name, city="Pittsburgh"):
		#data consists of restaurant name and city
		data = {}
		data['count'] = 1
		data['q'] = name
		if city is not None:
			data['entity_type'] = "city"
			data['entity_id'] = self.getLocationID(city)

                

		restaurants = self.makePOSTReq("/search", data)
		if restaurants['results_found'] == 0:
			return None
		self._restaurant = restaurants['restaurants'][0]['restaurant']
		self.loadComments()
		self._ldaModel.loadReviews(map(lambda r: r[0], self._reviews))

		return self._restaurant["name"]

	def getLocationID(self, city):
	    data = {}	
	    data['q'] = city
	    cities = self.makePOSTReq("/cities", data)
	    if len(cities["location_suggestions"]) == 0:
	        return None
	    return cities["location_suggestions"][0]["id"]  

	def loadComments(self):
		data = {}
		data['res_id'] = self._restaurant['id']
		data['count'] = 20
 
		reviews = self.makePOSTReq("/reviews", data)
		if reviews['reviews_shown'] == 0:
			return 
		self._reviews = list(map(lambda r: (r['review']['review_text'], r['review']['rating']), 
			reviews['user_reviews']))
		self._reviews.extend(yelpAPI.loadComments(
			self._restaurant["name"],
			self._restaurant["location"]["zipcode"]))



	def makePOSTReq(self, path, data):
		r = requests.post(self._url + path, headers = self._headers, params=data)
		return r.json()       
    