import os
from simplefont import sign_font
from pyledsign.minisign import MiniSign


class Array:
    def zero_one(self, data):
        zero_oned = ""
        for row in data:
            joined_row = "".join("{0}".format(n) for n in row)
            zero_oned += joined_row
        return zero_oned


class Slide:

    def __init__(self):
        pass

    def typeset(self, slide_text):
        self.slide_text = slide_text
        # font setup
        pwd = os.path.dirname(os.path.realpath(__file__))
        new_glyphs_path = '/'.join([pwd, 'fonts'])
        font = sign_font(new_glyphs_path)

        # sign setup
        portname = '/dev/ttyUSB0'
        sign = MiniSign(devicetype='sign', port=portname, )

        # THIS IS BREAKING WHEN THE TEXT IS TOO LONG
        # render message as bitmap
        matrix = font.render_multiline(self.slide_text, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
        if not matrix:
            return False
        text_to_set = Array().zero_one(matrix)
        self.typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_to_set)
        return self.typeset

    def writesign(self):
        # sign setup
        portname = '/dev/ttyUSB0'
        sign = MiniSign(devicetype='sign', port=portname, )

        # queue and send message
        sign.queuemsg(data="%s" % typeset, effect='hold');
        sign.sendqueue(device=portname, runslots='none')
