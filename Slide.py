class Array:
    def zero_one(self, data):
        zero_oned = ""
        for row in data:
            joined_row = "".join("{0}".format(n) for n in row)
            zero_oned += joined_row
        return zero_oned

class Slide(service):
    self.service = service

    def compose_lines(self): # format the two-line text message to display
        line2 = ''
        bus_format = '%s min'
        for bus in arrival_list:
            if bool(bus) is True:  # make sure there are predictions
                if ';' in bus['pt']:  # handle response of APPROACHING e.g. 0 mins prediction
                    bus['pt'] = '!0!'
                bus_entry = bus_format % (bus['pt'])
                line2 = line2 + ' ' + bus_entry  # append the arrival time for each bus e.g. '22 min'
            else:
                line2 = 'No arrivals next 30 mins.'
            degree_sign = u'\N{DEGREE SIGN}'
            temp_now = get_weather('Jersey City')  # hardcoded for now
            temp_msg = (temp_now['temp'] + degree_sign)
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) + ' ' + temp_msg
            lines = []
            lines.append(line1)
            lines.append('#' + bus['rd'] + line2)
            slide = lines[:2]
            slideshow.append(slide)

        def typeset(self): # renders a bitmap slide 16 x 96

            # font setup
            pwd = os.path.dirname(os.path.realpath(__file__))
            new_glyphs_path = '/'.join([pwd, 'fonts'])
            font = sign_font(new_glyphs_path)

            # sign setup
            portname = '/dev/ttyUSB0'
            sign = MiniSign(devicetype='sign', port=portname, )

            # THIS IS BREAKING WHEN THE TEXT IS TOO LONG
            # render message as bitmap
            matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
            if not matrix:
                return False
            text_for_sign = Array().zero_one(matrix)
            typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);

        def writesign(self):
            # queue and send message
            sign.queuemsg(data="%s" % typeset, effect='hold');
            sign.sendqueue(device=portname, runslots='none')




