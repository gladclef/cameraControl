import serial.tools.list_ports
import serial
import time
import winsound

class SerialConnection():
	conn = None # the serial.Serial value
	port = None # the comm port eg "COM3"

	def __init__(self):
		pass

	def __del__(self):
		if (not self.conn is None):
			self.conn.close()

	def requestUserConnection(self):
		ports = list(serial.tools.list_ports.comports())
		if (len(ports) == 0):
			print("no serial ports found with pyserial command serial.tools.list_ports.comports()")
			exit(1)

		choice = -1
		while (choice < 1 or choice > len(ports)):
			print("Please pick one of the following ports to connect to:")
			for i in range(len(ports)):
				print(str(i + 1) + ": " + str(ports[i]))
			try:
				choice = int(raw_input(">> "))
			except ValueError:
				print("value must be an integer")
			if (choice < 1 or choice > len(ports)):
				print("value must be between 1 and " + str(len(ports)))

		self.port = ports[choice - 1].device # eg "COM3"
		self.connect()

	def connect(self):
		try:
			self.conn = serial.Serial(self.port, 9600)
			read()
		except:
			print("Error connecting to port " + self.port + " with serial.Serial")
			exit(1)

	def getConnect(self):
		return self.conn

	def read(self):
		count = self.conn.in_waiting
		print(self.conn.read(count).decode("utf-8"), end='')
		return count

	def write(self, val):
		byteval = val.encode(encoding="utf-8")
		print("writing: " + byteval)
		self.conn.write(byteval)

		startTime = int(round(time.time() * 1000))
		while (self.read() == 0):
			time.sleep(0.1)
			currTime = int(round(time.time() * 1000))
			if (currTime - startTime > 10 * 1000):
				print("connection error, try starting the program again")
				for i in range(3):
					winsound.Beep(440, 250)
					time.sleep(0.25)
				exit(1)
			pass
		pass

	def setPan(self, relativePan):
		absPan = int((relativePan + 1.0) * (255.0 / 2.0))
		self.write("7:Cb09" + str(absPan))

	def setTilt(self, relativeTilt):
		absTilt = int((relativeTilt + 1.0) * (255.0 / 2.0))
		self.write("7:Cb10" + str(absTilt))

if __name__ == "__main__":
	serialConnection = SerialConnection()
	serialConnection.requestUserConnection()
	serialConnection.setPan(-1)
	time.sleep(1)
	serialConnection.setPan(-0.5)
	time.sleep(1)
	serialConnection.setPan(0)
	time.sleep(1)
	serialConnection.setPan(0.5)
	time.sleep(1)
	serialConnection.setPan(1)
	time.sleep(1)