import socket
import sys
import math
import errno
from multiprocessing import Process

def process_start(c_sockd):
	c_sockd.send(str.encode('Connected'))
	while True:
		data = c_sockd.recv(1024)
		data = data.decode('utf-8')
		num = c_sockd.recv(1024)
		try:
			num = float(num.decode('utf-8'))
		except:
			print('no input')
		if data == '1':
			result = math.log10(num)
		elif data == '2':
			result = math.sqrt(num)
		elif data == '3':
			result = math.exp(num)
		else:
			print('A client disconnected')
			break
		c_sockd.send(str.encode(str(result)))
	c_sockd.close()

if __name__ =='__main__':
	sockd = socket.socket()
	sockd.bind(('',8889))
	print('listening...')
	sockd.listen(3)
	try:
		while True:
			try:
				c_sockd, c_addr = sockd.accept()
				print('connected to {}'.format(c_addr))
				p = Process(target=process_start,args=(c_sockd,))
				p.start()
			except socket.error:
				print("socket error")
	except Exception as e:
		print('exception occured')
		print(e)
		sys.exit(1)
	finally:
		sockd.close()
