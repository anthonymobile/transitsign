import sys
from datetime import datetime

class Service:

    def __init__(self, stop, route):

        # passed
        self.stop = stop  # type: int
        self.route = route # type: int

        # init to be filled
        self.arrivals_list = []
        self.lines = []

        # computed
        self.arrival_data = self.get_arrivals()
        self.slide_text=self.compose_lines()

    def get_arrivals(self):
        import urllib.request, urllib.error, urllib.parse
        import xml.etree.ElementTree

        arrivals_url = 'http://mybusnow.njtransit.com/bustime/map/getStopPredictions.jsp?route=%s&stop=%s'
        submit_url = arrivals_url % (self.route, self.stop)
        # print submit_url

        try:
            data = urllib.request.urlopen(submit_url).read()
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            sys.exit('Exiting.')
        except urllib.error.URLError as e:
            print('We failed to reach a server. (internet down?)')
            sys.exit('Exiting.')
        else:
            pass
        # print data
        e = xml.etree.ElementTree.fromstring(data)

        x = e.findall('noPredictionMessage')

        if e.findall('noPredictionMessage'):
            self.arrivals_list.append('No service.')
            return self.arrivals_list

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

    def compose_lines(self):
        line2 = ''
        bus_format = '%s min'
        if self.arrivals_list[0]=='No service.':
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P'))
            line2 = 'No service'
            self.lines.append(line1)
            self.lines.append(line2)
            return self.lines

        for bus in self.arrival_data:
            if bool(bus) is True:  # make sure there are predictions
                if ';' in bus['pt']:  # handle response of APPROACHING e.g. 0 mins prediction
                    bus['pt'] = '!0!'
                bus_entry = bus_format % (bus['pt'])
                line2 = line2 + ' ' + bus_entry  # append the arrival time for each bus e.g. '22 min'
            else:
                line2 = 'No arrivals next 30 mins.'
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) # + ' ' + temp_msg
            self.lines.append(line1)
            self.lines.append('#' + bus['rd'] + line2)
            self.lines = self.lines[:2]

        return self.lines
