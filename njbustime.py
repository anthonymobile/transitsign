# LED screen bus arrival display
# scapes and parses NJT MyBusNow API XML to brightLEDsigns.com display

import urllib2, argparse, os, sys, datetime
import xml.etree.ElementTree
from signs import WriteSign, WriteBadge

#----------------------------------------------------------------------
# setup
#----------------------------------------------------------------------

arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'

now  = datetime.datetime.now()
route_id = 'all'
key = '0.3003391435305782'

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
parser.add_argument('-s', '--stop', dest='stop_id', required=True, help='NJTransit bus stop number')
# parser.add_argument('-r', '--route', dest='route_id_user', required=False, help='NJTransit bus route number')
parser.add_argument('-d', '--display', dest='display_type', default='sign', choices=['sign','badge'], required=True, help='brightLEDsigns.com display type')
parser.add_argument("-p", "--platform", choices=['pi', 'osx'], help="OS platform(required)", required=True, default='pi')
args = parser.parse_args()


#----------------------------------------------------------------------
# fetching and parsing data
#----------------------------------------------------------------------

def make_url (stop_id, route_id, key):

    submit_url = arrivals_url % (stop_id, route_id, key)

    return submit_url

def get_url (url):

    buses = urllib2.urlopen(url)
    print 'fetched url'
    
    return buses

def parse_arrivals(buses):

    data = buses

    arrivals = []

    e = xml.etree.ElementTree.fromstring(data)
    for atype in e.findall('pre'):
        fields = { }
        for field in atype.getchildren():
            if field.tag not in fields and hasattr(field, 'text'):
                if field.text is None:
                    fields[field.tag] = ''
                    continue
                fields[field.tag] = field.text

        arrivals.append(fields)

    return arrivals

#----------------------------------------------------------------------
# format outgoing message
#----------------------------------------------------------------------

def format_lines (display_type, arrivals):

    lines = []
    ogm_format = '%s   %s min'

    # for sign
    # show the final destination and arrival time for next 2 departures in the list, static
    if display_type == 'screen':
        for bus in arrivals:
            insert_line = _ogm_format % bus.fd, bus.pt
            lines.append(insert_line)   
        ogm = lines[:2]
        effect = 'hold'


    # for badge
    # show the final destination and arrival time for next departures in the list,  scroll
    elif display_type == 'badge':
        for bus in arrivals:
            insert_line = _ogm_format % bus.fd, bus.pt
            lines.append(insert_line)   
        ogm = lines[:1]
        effect = 'scroll'


    # n.b. lines has all the arrivals from API response
    # in case we want to use on a bigger screen

    # other fields of interest: bus.rn <rn>128</rn> Route number


    return ogm, effect

#----------------------------------------------------------------------
# send to LED
#----------------------------------------------------------------------

def show_buses (ogm,effect):

    speed=3

    try:
        if args.write == True:
            if args.display == 'sign':
                WriteSign(args.platform,ogm,effect,speed)

            elif args.display == 'badge':
                WriteBadge(args.platform,ogm,effect,speed)

        else:
            print 'END:: Write (-w) flag not set, not sending to LED.'

    except:
        print 'Error writing to sign. Are you sure its connected? Really are you sure?'

    return



#----------------------------------------------------------------------
# main program
#----------------------------------------------------------------------

'''try:
  args.route_id_user
except NameError:
  pass
else:
  route_id = args.route_id_user'''

print args.stop_id, route_id, key


parse_arrivals(get_url(make_url(args.stop_id, route_id, key)))

format_lines(display_type, arrivals)

show_buses(ogm, effect)

