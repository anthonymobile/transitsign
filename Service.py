class Service:


    def __init__(self, stop, route):
        self.stop = stop  # type: int
        self.route = route # type: int
        # self.forecast = forecast  # type: str


    def get_arrivals(self):
        import urllib2
        import xml.etree.ElementTree

        api_key = '0.3003391435305782'
        arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
        submit_url = arrivals_url % (self.route, self.stop, api_key)
        # print submit_url

        try:
            data = urllib2.urlopen(submit_url).read()
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            sys.exit('Exiting.')
        except urllib2.URLError, e:
            print 'We failed to reach a server. (internet down?)'
            sys.exit('Exiting.')
        else:
            pass
        # print data

        self.arrivals_list = []
        e = xml.etree.ElementTree.fromstring(data)
        for atype in e.findall('pre'):
            fields = {}
            for field in atype.getchildren():
                if field.tag not in fields and hasattr(field, 'text'):
                    if field.text is None:
                        fields[field.tag] = ''
                        continue
                    fields[field.tag] = field.text.replace("&nbsp", "")
            self.arrivals_list.append(fields)
        return self.arrivals_list


    def get_weather(self):
        import pyowm

        owm = pyowm.OWM('d03e7d5526d81ddc4c1b4ec24a1915c9')  # You MUST provide a valid API key

        try:
            observation = owm.weather_at_place(self.forecast)
            w = observation.get_weather()
            temps = w.get_temperature(unit='fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

            temp_report = "%.0f" % temps['temp']
            # degree_sign = u'\N{DEGREE SIGN}'
            # temp_msg = (temp_report + degree_sign)

        except:
            print('Couldnt reach the weather API endpoint. Internet down?')

        return temp_report


    def compose_lines(self):
        # format the two-line text message to display
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
            lines = lines[:2]

        return self.lines

