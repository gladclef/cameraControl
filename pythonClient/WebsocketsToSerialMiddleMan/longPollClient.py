import http.client, urllib.parse
import json
import random
from exceptions import PollingException
from socket import timeout
from json.decoder import JSONDecodeError

class longPollClient:
	clientId = random.randint(2, 10000000)
	lastMessageId = 0
	conn = None

	def __init__(self):
		self.initConn()

	def __del__(self):
		self.conn.close()
		self.conn = None

	def initConn(self):
		self.conn = http.client.HTTPSConnection('bbean.us', port=443, timeout=60)

	def reinitConn(self):
		if (self.conn != None):
			self.conn.close()
		self.initConn()

	def parseData(self, data):
		try:
			point = json.loads(data)
			point['pan'] = float(point['pan'])
			point['tilt'] = float(point['tilt'])
			point['pan_range'] = float(point['pan_range'])
			point['tilt_range'] = float(point['tilt_range'])
			point['pan_rel'] = (point['pan'] + point['pan_range']) / (point['pan_range'] * 2)
			point['tilt_rel'] = (point['tilt'] + point['tilt_range']) / (point['tilt_range'] * 2)
			self.lastMessageId = point['message_idx']
			return point
		except JSONDecodeError as e:
			print(data)
			raise PollingException(response, e)
		except Exception as e:
			raise PollingException(response, e)

	def getLatestPoint(self):
		times = {
			'prep': 0,
			'response': 0,
			'parse': 0
		}
		params = urllib.parse.urlencode({
			'command': 'subscribePanTilt',
			'camera': 'Derek DnD',
			'clientId': self.clientId,
			'lastMessageId': self.lastMessageId
		})
		headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*'}

		response = None
		gotResponse = False
		while (not gotResponse):
			gotResponse = True
			try:
				self.conn.request('POST', '/small/cameraControl/communication/longPoll/server.php', params, headers)
				response = self.conn.getresponse()
			except timeout:
				print("timeout")
				self.reinitConn()
				gotResponse = False
		
		if (response.status is 200):
			data = response.read()
			return self.parseData(data)
		else:
			raise PollingException(response, None)

if __name__ == "__main__":
	random.seed()
	client = longPollClient()
	try:
		for i in range(10):
			point = client.getLatestPoint()
			print(point)
	except Exception as e:
		print(e)