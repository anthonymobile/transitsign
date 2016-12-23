# find the Repleo USB port
# 

def serialfind():

	from subprocess import call
	dev = call('ls /dev | grep Repleo')

	# check if tty.usbserial exists (OSX)

	for line in dev:
		if (line == 'tty.usbserial' or line == 'tty.USBserial'):
			then tty = 'tty.usbserial'
		elif line == 'ttyUSB0':
			then tty = 'ttyUSB0'

	# if neither then check repleo
	dev = call('ls /dev | grep Repleo')

	for line in dev:
		if line[:3] = 'tty'
		then tty_handle = line

	return tty

