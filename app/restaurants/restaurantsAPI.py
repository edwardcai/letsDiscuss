import httplib
import urllib2
import json
import requests
import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from app.restaurants.yelpAPI import loadComments
from app.restaurants.lda.ldaModel import *
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator


class RestaurantsAPI(object):
	def __init__(self):
		self._url = "https://developers.zomato.com/api/v2.1"
		self._restaurant=None
		self._ldaModel = LdaModel()
		self._reviews = None


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
		params = {
	    	'term': name,
	      	'limit': 1
		}

		results = self.getYelpClient().search(city, **params)
 		if len(results.businesses) == 0:
			return None
		self._restaurant = results.businesses[0]

		self.loadComments()
		if len(self._reviews) == 0:
			return None
		self._ldaModel.loadReviews([review[0] for review in self._reviews])
		return self._restaurant.name

	def getLocationID(self, city):
	    data = {}	
	    data['q'] = city
	    cities = self.makePOSTReq("/cities", data)
	    if len(cities["location_suggestions"]) == 0:
	        return None
	    return cities["location_suggestions"][0]["id"]  

	def loadComments(self):
		
		self._reviews = loadComments(
			self._restaurant.name,
			self._restaurant.location.postal_code)  

	def makePOSTReq(self, path, data):
		r = requests.post(self._url + path, headers = self._headers, params=data)
		return r.json()       
    