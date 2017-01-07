# LED screen bus arrival display
# scapes and parses NJT MyBusNow API XML to brightLEDsigns.com display


import urllib2, argparse, os, sys, datetime
import xml.etree.ElementTree
from signs import WritePlaintext, WriteFonts

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
args = parser.parse_args()


#----------------------------------------------------------------------
# fetching and parsing data
#----------------------------------------------------------------------

submit_url = arrivals_url % (route_id, args.stop_id, key)

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
    # all is good

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



#----------------------------------------------------------------------
# format outgoing message
#----------------------------------------------------------------------

ogm = []
lines = []

# for larger LED sign, show headsign, and prediction for next 2 arrivals
if args.display_type == 'sign':
    ogm_format = '%s %s min'
    for bus in arrivals:
        dest_short = bus['fd'][:15]
        if ';' in bus['pt']: # fix for response of APPROACHING e.g. 0 mins prediction
            bus['pt'] = '!!'
        insert_line = ogm_format % (dest_short, bus['pt'])
        lines.append(insert_line) 
    ogm = lines[:2]
    effect = 'hold'

# for LED badge, show route number and integer for next arrival
if args.display_type == 'badge':
    ogm_format = '%s %s'
    for bus in arrivals:
        dest_short = (bus['pt'])
        insert_line = ogm_format % (dest_short, bus['pt'])
        lines.append(insert_line) 
    ogm = lines[:2]
    effect = 'hold'


#----------------------------------------------------------------------
# send to LED
#----------------------------------------------------------------------

speed=4

try:
    if args.write == True:
        if args.display_type == 'sign':
            WriteFonts(ogm,effect,speed)

        elif args.display_type == 'badge':
            WritePlaintext(ogm,effect,speed)

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
