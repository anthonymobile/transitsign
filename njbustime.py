# LED screen bus arrival display
# scapes and parses NJT MyBusNow API XML to brightLEDsigns.com display

# test command 
# python njbustime.py -s 21374 -d sign -p osx -w
# python njbustime.py -s 21374 -d sign -p pi -w

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

submit_url = arrivals_url % (route_id, args.stop_id, key)
print ('fetching %s' % submit_url)

data = urllib2.urlopen(submit_url).read()

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



#----------------------------------------------------------------------
# format outgoing message
#----------------------------------------------------------------------

ogm = []
lines = []
ogm_format = '%s   %s min'

# sign
# show the final destination and arrival time for next 2 departures in the list, static
if args.display_type == 'sign':
    n = 0
    for bus in arrivals:
        #
        # truncate bus['fd'] here for screen size. may be too conservative
        #
        dest_short = bus['fd'][:15]
        insert_line = ogm_format % (dest_short, bus['pt'])
        lines.append(insert_line) 
        n +=1  
    print ('Found %s buses arriving soon.' % n)
    ogm = lines[:2]
    effect = 'hold'

#  badge
# show the final destination and arrival time for next departures in the list,  scroll
if args.display_type == 'badge':
    print 'Formatting OGM for LED screen...'
    for bus in arrivals:
        insert_line = ogm_format % bus.fd, bus.pt
        lines.append(insert_line)
    ogm = lines[:1]
    effect = 'scroll'

print ogm

# n.b. lines has all the arrivals from API response
# in case we want to use on a bigger screen

# other fields of interest: bus.rn <rn>128</rn> Route number

#----------------------------------------------------------------------
# send to LED
#----------------------------------------------------------------------

speed=3

try:
    if args.write == True:
        if args.display == 'sign':
            WriteSign(args.platform,ogm,effect,speed)

        elif args.display == 'badge':
            WriteBadge(args.platform,ogm,effect,speed)

    else:
        print ('---OGM-----------------')
        print ogm
        print 'END:: Write (-w) flag not set, not sending to LED.'

except:
    print ('---OGM-----------------')
    print ogm
    print 'Error writing to sign. Are you sure its connected? Really are you sure?'

