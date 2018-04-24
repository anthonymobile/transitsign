

class Service (stop, route):
    self.stop = stop  # type: int
    self.route = route # type: int

    def get_arrivals:
        import urllib2,
        import xml.etree.ElementTree

        for service in service_specs:
            # create the url
            api_key = '0.3003391435305782'
            arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
            submit_url = arrivals_url % (service[2], service[1], api_key)
            print submit_url

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
            arrival_list = []
            e = xml.etree.ElementTree.fromstring(data)
            for atype in e.findall('pre'):
                fields = {}
                for field in atype.getchildren():
                    if field.tag not in fields and hasattr(field, 'text'):
                        if field.text is None:
                            fields[field.tag] = ''
                            continue
                        fields[field.tag] = field.text.replace("&nbsp", "")
                arrival_list.append(fields)

    def get_weather:
        from weather import get_weather

