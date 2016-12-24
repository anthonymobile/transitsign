# sets the USB serial port ttyhandle
# default for linux is /dev/ttyUSB0
# for OSX, search for a Repleo driver handle
# otherwise default is /dev/tty.usbserial if it exists

def serialfind():

	import platform, os, re

	# 1 figure out platform
	platform_name = platform.system()

	if platform_name == 'Darwin':
		
		# look for a Repleo driver
		dev_contents = os.listdir('/dev')
		for line in dev_contents:
	        if not "Repleo" in line:
	           continue
	        try:
	            tty_handle = ('/dev/'+str(line))
	        except IndexError:
	            print 'IndexError, whatever that is'

		# look for /dev/tty.usbserial in /dev
	    if tty_handle not exists:
			for line in dev_contents:
				if 'tty.usbserial' in line:
					tty_handle = '/dev/tty.usbserial'


	elif platform_name == 'Linux':
		tty_handle = '/dev/ttyUSB0'

	return tty_handle
