import defaultWebsocketApp
import CurrentValue
import message
import SerialConnection
import json
import queue
import time
import threading

class MessageHandler():
	messageQueue = None
	pan = 0.0
	tilt = 0.0
	currentValue = None
	serialConnection = None
	timer = None
	lock = threading.Lock()

	def __init__(self, currentValue, serialConnection):
		self.messageQueue = queue.Queue()
		self.currentValue = currentValue
		self.serialConnection = serialConnection

	def putMessage(self, msg):
		self.messageQueue.put(msg)
		droppedMsg = None
		if (self.messageQueue.qsize() > 5):
			droppedMsg = self.messageQueue.get()
		#print("queue size: " + str(self.messageQueue.qsize()) + ", dropped: " + str(droppedMsg))

	def handleMessage(self, ws, msgStr):
		print("received message, ", end='')
		msg = message.Message(msgStr)
		self.pan = msg.getRelativePan(self.currentValue.getPanRange())
		self.tilt = msg.getRelativeTilt(self.currentValue.getTiltRange())
		print("pan=" + str(self.pan) + ", tilt=" + str(self.tilt))
		self.putMessage(msg)
		self.update()

	def update(self):
		with self.lock:
			if (self.timer is None):
				self.timer = threading.Timer(0.05, self.doCommunication)
				self.timer.start()

	def doCommunication(self):
		with self.lock:
			self.serialConnection.setPan(self.pan)
			self.serialConnection.setTilt(self.tilt)
			self.timer.cancel()
			self.timer = None

if __name__ == "__main__":
	serialConnection = SerialConnection.SerialConnection()
	serialConnection.requestUserConnection()
	cv = CurrentValue.CurrentValue()
	handler = MessageHandler(cv, serialConnection)
	app = defaultWebsocketApp.defaultWebsocketApp(handler.handleMessage)
	app.start()