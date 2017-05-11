from app.restaurants.restaurantsAPI import *

class Dialogue(object):
	class States:
		SEARCH = 1
		DISCUSS = 2
		
	def __init__(self):
		self._state = self.States.SEARCH
		self._restaurantsAPI = RestaurantsAPI()
                self._hasRecommended = False


	def getResponse(self, query):
		if self._state == self.States.SEARCH:
			restaurant = self._restaurantsAPI.search(query)
			if restaurant is None:
				return ("Sorry, I do not know that restaurant", "")
			self._state = self.States.DISCUSS
			return ("Sure, let's talk about " + restaurant, "")
		if self._state == self.States.DISCUSS:
			#Go back to restaurant search 
			if query.lower() in {"thank you", "thanks", "exit", "quit", "goodbye", "good bye"} :
				self._state = self.States.SEARCH
                                self._hasRecommended = False
				return ("What restaurant would you like to talk about?", "")
                        if query.lower() in {"yes", "yes please", "sure", "ok", "okay", "sounds good", "sure thing", "yeah", "yep", "ya"}:
                            return self._restaurantsAPI.discuss()
                        elif query.lower() in {"no", "no thanks", "no thank you", "nope", "nah", "na"}:
                            return ("What about the restaurant do you want to talk about?", "")
                        else:
                            self.has_recommended = True
                            return self._restaurantsAPI.discuss(query)
