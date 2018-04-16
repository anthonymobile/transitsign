from pyledsign.minisign import MiniSign

portname = '/dev/ttyUSB0'

print portname

from pyledsign.minisign import MiniSign
mysign = MiniSign(
    devicetype='sign',
)
# queue up a text message
print 'testing TEXT mode output'

mysign.queuemsg(
    data='Hello World'
)
# queue up a second message
#   - using the optional effect parameter.
#     if not supplied, defaults to 'scroll'
mysign.queuemsg(
    data='MSG 2',
    effect='snow'
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
print 'done TEXT mode test'




# queue up a rendered font
print 'testing FONT mode output'

# LED DISPLAY the test from the docs

from pyledsign.minisign import MiniSign
mysign = MiniSign(
    devicetype='sign',
    port='/dev/ttyUSB0',
)
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
# now use that in a message
mysign.queuemsg(
    data="a 5 pixel box: %s" % pic
);
mysign.sendqueue(
    device='/dev/ttyUSB0'
)


# random 16 by 96 box of pixels (the sign's dimensions)

# LED DISPLAY the test from the docs

from pyledsign.minisign import MiniSign
mysign = MiniSign(
    devicetype='sign',
    port='/dev/ttyUSB0',
)
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
mysign.queuemsg(
    data="%s" % pic
);
mysign.sendqueue(
    device='/dev/ttyUSB0'
)

'''
# try to render something with fonts library
# max width of the image is 256 pixels (sign only is 16 pixels high by 96 pixels wide)

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
new_glyphs_path = '/'.join([pwd,'fonts'])
font = sign_font(new_glyphs_path)

# sign setup
portname = '/dev/ttyUSB0'
mysign = MiniSign(devicetype='sign',)

# sign screen_height hardcoded for now, better if it can be pulled from 
# the MiniSign class instance 'sign'
matrix = font.render_multiline(lines, 16 / 2,{"ignore_shift_h" : True, "fixed_width" : 96})
if not matrix:
    return False

# typeset the OGM as an image
# pyledsign may not accept images this big -- may need to break it up
text_for_sign = Array().zero_one(matrix)
typeset=mysign.queuepix(height=len(matrix), width =len(matrix[0]), data  = text_for_sign);

# send to sign
mysign.queuemsg(data="%s" % typeset, effect=effect)
mysign.sendqueue(device=portname)
time.sleep(6)
'''

print 'done FONT mode test'

