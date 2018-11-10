import json
import time

class Message():
	pan = 0.0
	tilt = 0.0
	clientId = 0
	index = 0
	time = 0

	def __init__(self, msgJSON):
		msg = json.loads(msgJSON)
		self.pan = float(msg["pan"])
		self.tilt = float(msg["tilt"])
		self.clientId = int(msg["clientId"])
		self.messageIndex = int(msg["messageIndex"])
		self.time = int(round(time.time() * 1000))

	def getPan(self):
		return self.pan

	def getTilt(self):
		return self.tilt

	def getRelativePan(self, panRange):
		return self.pan / panRange

	def getRelativeTilt(self, tiltRange):
		return self.tilt / tiltRange

	def getClientId(self):
		return self.clientId

	def getIndex(self):
		return self.index

	def getTime(self):
		return self.time

if __name__ == "__main__":
	msg = Message("{\"pan\":-76,\"tilt\":58,\"remote\":false,\"clientId\":4714,\"messageIndex\":1}")
	print("pan: " + str(msg.getPan()))
	print("tilt: " + str(msg.getTilt()))
	print("relative pan to 200: " + str(msg.getRelativePan(200)))
	print("relative tilt to 100: " + str(msg.getRelativeTilt(100)))
	print("clientId: " + str(msg.getClientId()))
	print("messageIndex: " + str(msg.getIndex()))
	print("recieved at: " + str(msg.getTime()))

