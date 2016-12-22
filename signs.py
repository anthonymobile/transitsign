# sign.py

from pyledsign.minisign import MiniSign
from simplefont import sign_font

def WriteSign(platform,lines,effect,speed):
	
	# need later to format the ogm
	class Array:
		def zero_one(self, data):
			zero_oned = ""
			for row in data:
				joined_row = "".join("{0}".format(n) for n in row)
				zero_oned += joined_row
			return zero_oned

	# font setup
	pwd = os.path.dirname(os.path.realpath(__file__))
	new_glyphs_path = '/'.join([pwd,'glyphs'])
	
	# sign setup
	if platform == 'osx':
		portname = '/dev/tty.usbserial'
	else:
		portname ='/dev/ttyUSB0'
	sign = MiniSign(devicetype='sign', port=portname,)

	font = sign_font(new_glyphs_path)

	# sign screen_height hardcoded for now, better if it can be pulled from 
	# the MiniSign class instance 'sign'
	# e.g. sign.SCREEN_HEIGHT / 2, or some such
	# hardcoded for now original code below, again shoud be pulled ideally 
	# from the class instance
	# "fixed_width" : LEDSign.SCREEN_WIDTH
	matrix = font.render_multiline(lines, 16 / 2,{"ignore_shift_h" : True, "fixed_width" : 96})

	if not matrix:
		return False
	
	text_for_sign = Array().zero_one(matrix)
	typeset=sign.queuepix(height=len(matrix), width =len(matrix[0]), data  = text_for_sign);
	sign.queuemsg(data="%s" % typeset, effect=effect);
	sign.sendqueue(device=portname)

	time.sleep(6)


def WriteBadge(platform,lines,effect,speed):

# send simple text messages

	print platform,lines,effect,speed

	if platform == 'osx':
		portname = '/dev/tty.usbserial'
	else:
		portname ='/dev/ttyUSB0'

	print portname
	'''
	badge = MiniSign(devicetype='sign',)
	badge.queuemsg(data=line)
	badge.sendqueue(device=portname)

	time.sleep(6)
	'''

	mysign = MiniSign(
	    devicetype='sign',
	)
	# queue up a text message
	mysign.queuemsg(
	    data=lines[0]
	)
	# queue up a second message
	#   - using the optional effect parameter.
	#     if not supplied, defaults to 'scroll'
	mysign.queuemsg(
	    data='MSG 2',
	)
	#
	# send the message to the sign via the serial port
	#   note that the sendqueue() method does not empty
	#   the buffer, so if we have a second sign, on a 
	#   different serial port, we can send everything
	#   to it as well...
	#
	mysign.sendqueue(
	    device=portname
	)


