class PollingException(Exception):
	"""Used by longPollClient when getting the latest point fails"""
	response = None
	jsonException = None

	def __init__(self, response, jsonException):
		self.response = response
		self.jsonException = jsonException

	def __str__(self):
		if (self.jsonException == None):
			return "PollingException (response " + str(self.response.status) + ": " + self.response.reason + ")"
		else:
			return "PollingException (json error " + str(self.jsonException) + ")"