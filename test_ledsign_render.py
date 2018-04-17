from pyledsign.minisign import MiniSign
import sys, time, os
import serialfind


# TEST 3

# test message
lines=['Webster/Congress','(119) 1m (85) 13m']


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
new_glyphs_path = '/'.join([pwd, 'fonts'])
font = sign_font(new_glyphs_path)

# sign setup
portname = serialfind.serialfind()
print portname
sign = MiniSign(devicetype='sign', port=portname, )

# render message
matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
text_for_sign = Array().zero_one(matrix)
typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);

# DEBUGGING
print matrix


# queue and send message
sign.queuemsg(data="%s" % typeset, effect='hold');
sign.sendqueue(device=portname)

# pause and report
time.sleep(6)
print 'done FONT mode test'