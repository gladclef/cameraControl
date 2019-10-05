import http.client, urllib.parse
import json
import random
from exceptions import PollingException

class longPollClient:
	clientId = random.randint(2, 10000000)
	lastMessageId = 0

	def getLatestPoint(self):
		params = urllib.parse.urlencode({
			'command': 'subscribePanTilt',
			'camera': 'Derek DnD',
			'clientId': self.clientId,
			'lastMessageId': self.lastMessageId
		})
		headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*'}
		conn = http.client.HTTPSConnection('bbean.us', port=443, timeout=60)
		conn.request('POST', '/small/cameraControl/communication/longPoll/server.php', params, headers)
		response = conn.getresponse()
		if (response.status is 200):
			data = response.read()
			conn.close()
			try:
				point = json.loads(data)
				point['pan'] = float(point['pan'])
				point['tilt'] = float(point['tilt'])
				point['pan_range'] = float(point['pan_range'])
				point['tilt_range'] = float(point['tilt_range'])
				point['pan_rel'] = (point['pan'] + point['pan_range']) / (point['pan_range'] * 2)
				point['tilt_rel'] = (point['tilt'] + point['tilt_range']) / (point['tilt_range'] * 2)
				return point
			except Exception as e:
				raise PollingException(response, e)
		else:
			conn.close()
			raise PollingException(response, None)

if __name__ == "__main__":
	random.seed()
	client = longPollClient()
	try:
		point = client.getLatestPoint()
		print(point)
	except Exception as e:
		print(e)