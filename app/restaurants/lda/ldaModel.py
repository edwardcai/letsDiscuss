import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models
import gensim
import random
import json
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer




class LdaModel:
	def __init__(self):
		self.ldaPath = "_stem40"

		#Needed for tokenizing
		self.stop_words = self.getStopwords()
		#self.lem = WordNetLemmatizer()
		self.stemmer = PorterStemmer()	
		self.translate_table = dict((ord(char), None) for char in string.punctuation)   
		self.dictionary = corpora.Dictionary.load("app/restaurants/lda/savedModel/dict" + self.ldaPath, mmap='r')
		#self.ldamodel = gensim.models.ldamodel.LdaModel.load("app/restaurants/lda/savedModel/lda2", mmap='r')
		self.ldaPath = "_stem40"
		self.totalWeights = None
		self.reviews = None
		self.sortedReviews = None

	def getStopwords(self):
		with open("app/restaurants/lda/stopwords.txt", "rU") as f:
			stopwords = set([line.strip() for  line in f])
		return stopwords

	#Given tokens, returns the document topics and their weights
	def getTopics(self, review, ldamodel):
		#Get rid of punctuation
		if isinstance(review, str):
			review = review.translate(None, string.punctuation)
		else:
			review = review.translate(self.translate_table)
		tokens = nltk.word_tokenize(review.lower())
		stopped_tokens = [i for i in tokens if not i in self.stop_words]
		stemmed_tokens = [self.stemmer.stem(i) for i in stopped_tokens]
		print(stemmed_tokens)
		bow = self.dictionary.doc2bow(stemmed_tokens)
		return ldamodel.get_document_topics(bow, minimum_probability=0)

	#Given a review, returns the most likely topic
	def getTopTopic(self, review):
		ldamodel = gensim.models.ldamodel.LdaModel.load("app/restaurants/lda/savedModel/lda" + self.ldaPath, mmap='r')
		topics = self.getTopics(review, ldamodel)
		topTopic = max(topics, key=lambda t: t[1])
		print topTopic
		return topTopic[0]

	#Given a list of reviews, sentence tokenizes them, and sorts them
	#according to the likeliness of being in each topic.
	def loadReviews(self, reviews):
		ldamodel = gensim.models.ldamodel.LdaModel.load("app/restaurants/lda/savedModel/lda" + self.ldaPath, mmap='r')
		self.reviews = nltk.sent_tokenize(" ".join(reviews))
		reviewsWithTopics = [(index, self.getTopics(review, ldamodel)) for (index,review) in enumerate(self.reviews)]
		self.sortedReviews = [map(lambda s: s[0],
						sorted(reviewsWithTopics, key = lambda r : r[1][index][1]))
						 for index in xrange(ldamodel.num_topics)]

		totalWeights = [0] * ldamodel.num_topics
		for review in reviewsWithTopics:
			topics = review[1]
			for topic in topics:
				topicID = topic[0]
				topicWeight = topic[1]
				totalWeights[topicID] += topicWeight
		totalWeights = zip(range(ldamodel.num_topics), totalWeights)
		self.talkingPoints = sorted(totalWeights, key=lambda w: w[1])[-8:]
		print(self.talkingPoints)
		# self.filteredReviews = [[] for i in xrange(ldamodel.num_topics)] 
		# for r in reviewsWithTopics:
		# 	review = r[0]
		# 	topics = r[1]
		# 	for t in topics:
		# 		topic = t[0]
		# 		weight = t[1]
		# 		if weight > 0.1:
		# 			self.filteredReviews[topic].append((review, weight))

		# for topic in ldamodel.print_topics(num_topics=ldamodel.num_topics, num_words=10):
		# 	print(topic)

	def idToTopic(self, topicID):
		with open("app/restaurants/lda/savedModel/labels" + self.ldaPath + ".json", "rU") as f:
			idDict = json.load(f)
			return idDict[str(topicID)]

	def generateRecommendedTopic(self):
		if self.talkingPoints == None:
			return None
		self.talkingPoint = random.choice(self.talkingPoints)[0]
		return self.idToTopic(self.talkingPoint) 

	def getRecommendedTopic(self):
		return self.talkingPoint
		

	def getTopReview(self, topic):
		reviews = self.sortedReviews[topic]
		if len(reviews) == 0:
			"Sorry, I don't have an opinion for that"
		review_index = reviews.pop()
		return self.reviews[review_index]

if __name__ == '__main__':
	ldaModel = LdaModel()
	print(ldaModel.getTopTopic("I want some food"))
