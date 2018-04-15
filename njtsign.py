# LED screen bus arrival display
# scapes and parses NJT MyBusNow API XML to brightLEDsigns.com display

import urllib2, argparse, os, sys
from datetime import datetime   
import xml.etree.ElementTree
from sign_handler import WritePlaintext, WriteFonts


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
parser.add_argument('-s', '--stop', dest='stop_id', required=True, help='NJTransit bus stop number')
parser.add_argument('-r', '--route', dest='route_id', required=False, help="NJTransit bus route number (if omitted=ALL)")
# parser.add_argument('-d', '--display', dest='display_type', default='sign', choices=['sign','badge'], required=True, help='brightLEDsigns.com display type')
args = parser.parse_args()

# fetching and parsing data
# right now shows all buses for a single stop
# direction is implicit

route_id = 'all'
if args.route_id > 0:
    route_id = args.route_id
now  = datetime.now() 
api_key = '0.3003391435305782'
arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
submit_url = arrivals_url % (route_id,args.stop_id,api_key)
print submit_url

try:
    data = urllib2.urlopen(submit_url).read()
except urllib2.HTTPError, e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
    sys.exit('Exiting.')
except urllib2.URLError, e:
    print 'We failed to reach a server. (internet down?)'
    ogm = []
    ogm.append('offline')
    WritePlaintext(ogm,'hold',3)
    # print 'Reason: ', e.reason

    sys.exit('Exiting.')
else:
    pass

arrivals = []

e = xml.etree.ElementTree.fromstring(data)
for atype in e.findall('pre'):
    fields = { }
    for field in atype.getchildren():
        if field.tag not in fields and hasattr(field, 'text'):
            if field.text is None:
                fields[field.tag] = ''
                continue
            fields[field.tag] = field.text.replace("&nbsp", "")

    arrivals.append(fields)


# format outgoing message (big sign only)
#
# 8:28am Wesbter & Congress
# 119 3m 6m 19m 85 24m
#

line2 = ''
bus_format = '#%s %s min '
for bus in arrivals:
    print bus
    if ';' in bus['pt']: # fix for response of APPROACHING e.g. 0 mins prediction
        bus['pt'] = '0!'
    bus_entry = bus_format % (bus['rd'], bus['pt'])
    line2 = line2 + bus_entry
ogm = []
lines = []
line1 = (datetime.now().strftime('%I:%M %p')) + '  Congress St & Webster Av'
lines.append(line1)
lines.append(line2)
ogm = lines[:2]
print ogm
effect = 'hold'
speed=4

# send to LED

try:
    if args.write == True:        
        WriteFonts(ogm,effect,speed)

    else:
        pass
        print ('---OGM TEST-----------------')
        print 'END:: Write (-w) flag not set, not sending to LED.'
        print ogm

except:
    print ('---OGM ERROR-----------------')
    print 'Error writing to sign. Are you sure its connected? Really are you sure?'
    print ogm
    pass
