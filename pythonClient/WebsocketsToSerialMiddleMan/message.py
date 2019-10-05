import json
import time

class Message():
	pan = 0.0
	tilt = 0.0
	pan_range = 0.0
	tilt_range = 0.0
	clientId = 0
	index = 0
	time = 0

	def __init__(self, msgJSON):
		msg = msgJSON#json.loads(msgJSON)
		self.pan = float(msg["pan"])
		self.tilt = float(msg["tilt"])
		self.pan_range = float(msg["pan_range"])
		self.tilt_range = float(msg["tilt_range"])
		self.clientId = int(msg["clientId"])
		self.messageIndex = int(msg["message_idx"])
		self.time = int(round(time.time() * 1000))

	def getPan(self):
		return self.pan

	def getTilt(self):
		return self.tilt

	def getRelativePan(self):
		return self.pan / self.pan_range#(self.pan + self.pan_range) / (self.pan_range * 2)

	def getRelativeTilt(self):
		return self.tilt / self.tilt_range#(self.tilt + self.tilt_range) / (self.tilt_range * 2)

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

