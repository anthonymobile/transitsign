import os






class Slide:

    def __init__(self, slide_text, sign):
        self.slide_text = slide_text
        self.sign = sign

    def typeset(self):

        # font setup
        pwd = os.path.dirname(os.path.realpath(__file__))
        new_glyphs_path = '../'.join(['fonts'])
        font = sign_font(new_glyphs_path)

        # render message as bitmap
        matrix = font.render_multiline(self.slide_text, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
        if not matrix:
            return False
        text_to_set = Array().zero_one(matrix)
        self.typeset = self.sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_to_set)
        return

