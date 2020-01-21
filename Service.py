import sys
from datetime import datetime

class Service:

    def __init__(self, stop, route, badge, rt_display):

        # passed
        self.stop = stop  # type: int
        self.route = route # type: int
        self.badge = badge # type: boolean
        self.rt_display = rt_display # type: boolean

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
        # trim anything more than first 2 arrivals
        self.arrivals_list=self.arrivals_list[:2]
        return self.arrivals_list

    def compose_lines(self):
        line2 = ''
        bus_format = '%s min '
        if self.arrivals_list[0]=='No service.':
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P'))
            line2 = '{a}. No arrivals'.format(a=self.route)
            self.lines.append(line1)
            self.lines.append(line2)
            return self.lines
        else:
            for bus in self.arrival_data:
                if bool(bus) is True:  # make sure there are predictions
                    if 'APPROACHING' in bus['pt']:
                        bus['pt'] = '!0!'
                    # if ';' in bus['pt']:  # handle response of APPROACHING e.g. 0 mins prediction
                    #     bus['pt'] = '!0!'
                    bus_entry = bus_format % (bus['pt'].split(' ')[0])
                    try:
                        # append the arrival time for each bus e.g. '22 min'
                        if self.badge == True:
                            # line2 = bus_entry
                            line2 = line2 + bus_entry
                        elif self.badge == False:
                            line2 = line2 + bus_entry  # append the arrival time for each bus e.g. '22 min'

                    except:
                        # if its too long, we dont add this bus and continue the loop
                        pass
                    continue
                else:
                    line2 = 'No arrivals next 30 mins.'
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) # + ' ' + temp_msg
            self.lines.append(line1)

            if self.badge == True:

                if self.rt_display == True:
                    # self.lines.append(line2) # works
                    self.lines.append(line2)
                elif self.rt_display == False:
                    # self.lines.append(line2) # works
                    self.lines.append(bus['rd'] + '. ' + line2)

            elif self.badge == False:
                self.lines.append(bus['rd'] + '. ' + line2)




            self.lines = self.lines[:2]

            # todo blink if under 3 minutes for 85, 5 for 87

            #todo add time
            # if there is room, add time to the rightmost on line 1 or 2

            return self.lines
