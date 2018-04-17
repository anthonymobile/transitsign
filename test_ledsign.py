from pyledsign.minisign import MiniSign

portname = '/dev/ttyUSB0'
print portname


# TEST 1 - PLAIN TEXT

mysign = MiniSign(devicetype='sign',port=portname,)
# queue up a text message (the weather -- see https://pyowm.readthedocs.io/en/latest/)
# from weather import get_weather

# forecast = get_weather('07307')
# print 'The forecast for JC Heights is %s' % forecast

mysign.queuemsg(data='Hello World')
# queue up a second message
#   - using the optional effect parameter.
#     if not supplied, defaults to 'scroll'
mysign.queuemsg(data='Is it snowing yet?',effect='snow')
#
# send the message to the sign via the serial port
#   note that the sendqueue() method does not empty
#   the buffer, so if we have a second sign, on a 
#   different serial port, we can send everything
#   to it as well...
#
mysign.sendqueue(device=portname)
print 'done TEXT mode test'



# TEST 2 - RENDERED FONT SMALL
# the test from the docs

print 'testing FONT mode output'

from pyledsign.minisign import MiniSign
mysign = MiniSign(devicetype='sign',)
# make a 5x5 pixel outlined box 
# height max is 256
pic=mysign.queuepix(
      height=5,
      width =5,
      data  =
        "11111" \
        "10001" \
        "10001" \
        "10001" \
        "11111"
);

mysign.queuemsg(data="a 5 pixel box: %s" % pic);
mysign.sendqueue(device=portname)


# TEST 3 - RENDERED FONT FULL SCREEN
# now use that in a message
# random 16 by 96 box of pixels (the sign's dimensions)

mysign = MiniSign(devicetype='sign',)
# make a 16 by 96 pixel outlined box 
# height max is 256

pic=mysign.queuepix(
      height=16,
      width =96,
      data  =
        "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" \
        "100011000101100011000101100011000101100011000101100011000101100011000101100011000101100011000101" \
        "100011000111100011000111100011000111100011000111100011000111100011000111100011000111100011000111" \
        "100011000100100011000100100011000100100011000100100011000100100011000100100011000100100011000100" \
       	"111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" \
        "100011000101100011000101100011000101100011000101100011000101100011000101100011000101100011000101" \
        "100011000111100011000111100011000111100011000111100011000111100011000111100011000111100011000111" \
        "100011000100100011000100100011000100100011000100100011000100100011000100100011000100100011000100" \
        "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" \
        "100011000101100011000101100011000101100011000101100011000101100011000101100011000101100011000101" \
        "100011000111100011000111100011000111100011000111100011000111100011000111100011000111100011000111" \
        "100011000100100011000100100011000100100011000100100011000100100011000100100011000100100011000100" \
       	"111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111" \
        "100011000101100011000101100011000101100011000101100011000101100011000101100011000101100011000101" \
        "100011000111100011000111100011000111100011000111100011000111100011000111100011000111100011000111" \
        "111111111100111111111100111111111100111111111100111111111100111111111100111111111100111111111100"
);
# now use that in a message
mysign.queuemsg(data="%s" % pic);
mysign.sendqueue(device=portname)

sys.exit()

# try to render something with fonts library
#

'''
# font setup
from simplefont import sign_font
pwd = os.path.dirname(os.path.realpath(__file__))
new_glyphs_path = '/'.join([pwd,'fonts'])
font = sign_font(new_glyphs_path)

# sign setup -- sign only is 16 pixels high by 96 pixels wide
mysign = MiniSign(devicetype='sign',)
portname = '/dev/ttyUSB0'


IS THIS STUFF FROM THE ORIGINAL PERL SIGN APP?

# prepare content receptacle
matrix = font.render_multiline(lines, 8,{"ignore_shift_h" : True, "fixed_width" : 96})

    if not matrix:
        return False

class Array:
    def zero_one(self, data):
        zero_oned = ""
        for row in data:
            joined_row = "".join("{0}".format(n) for n in row)
            zero_oned += joined_row
        return zero_oned



# typeset the OGM
text_for_sign = Array().zero_one(matrix)
typeset=mysign.queuepix(height=len(matrix), width =len(matrix[0]), data  = text_for_sign);


# send to sign
mysign.queuemsg(data="%s" % typeset, effect=effect)
mysign.sendqueue(device=portname)
time.sleep(6)


print 'done FONT mode test'
'''

# def OGM_Write(platform, lines, effect, speed):
# need later to format the ogm
class Array:
    def zero_one(self, data):
        zero_oned = ""
        for row in data:
            joined_row = "".join("{0}".format(n) for n in row)
            zero_oned += joined_row
        return zero_oned

# font setup
from simplefont import sign_font
pwd = os.path.dirname(os.path.realpath(__file__))
new_glyphs_path = '/'.join([pwd, 'glyphs'])

# sign setup
portname = '/dev/ttyUSB0'
sign = MiniSign(devicetype='sign', port=portname, )

font = sign_font(new_glyphs_path)

# sign screen_height hardcoded for now
matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})

text_for_sign = Array().zero_one(matrix)
typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);
sign.queuemsg(data="%s" % typeset, effect='hold');
sign.sendqueue(device=portname)

time.sleep(6)
