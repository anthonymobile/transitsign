# find the Repleo USB port
# 

def SerialFind(platform):

	from subprocess import call

	if platform == 'osx':
		searchstring = 'Repleo'

	dev = call('ls /dev')

	# check if tty.usbserial exists (OSX)

	for line in dev:
		if (line == 'tty.usbserial'):
			then tty = '/dev/tty.usbserial'
		elif line == 'ttyUSB0':
			then tty = '/dev/ttyUSB0'

	# if neither then check Repleo
	dev = call('ls /dev | grep %s') % searchstring

	for line in dev:
		if line[:3] = 'tty'
		then tty_handle = ('/dev/'+str(line))

	return tty

