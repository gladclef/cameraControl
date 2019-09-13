import json
import urllib.request

class CurrentValue():
	url = "https://bbean.us/small/cameraControl/index.php?printAsJSON"
	camera = {}

	def __init__(self):
		requestBytes = urllib.request.urlopen(self.url).read()
		requestJSON = requestBytes.decode("utf-8")
		self.camera = json.loads(requestJSON)
		self.toIntegers()

	def toIntegers(self):
		for a in self.camera:
			try:
				val = float(self.camera[a])
				self.camera[a] = val
			except ValueError:
				pass

	def getPanRange(self):
		return self.camera["pan_range"]

	def getTiltRange(self):
		return self.camera["tilt_range"]

	def getPan(self):
		return self.camera["pan"]

	def getTilt(self):
		return self.camera["tilt"]

	def getName(self):
		return self.camera["name"]

if __name__ == "__main__":
    cv = CurrentValue()
    print("pan range: " + str(cv.getPanRange()))
    print("tilt range: " + str(cv.getTiltRange()))