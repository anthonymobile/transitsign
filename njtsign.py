# LED screen bus arrival display
# scrapes and parses NJT MyBusNow API XML to brightLEDsigns.com display
# single stop, single route for now

import urllib2, argparse, os, sys
from datetime import datetime   
import xml.etree.ElementTree
from sign_handler import WriteText, WriteFont
from weather import get_weather


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
parser.add_argument('-s', '--stop', dest='stop_id', required=True, help='NJTransit bus stop number')
parser.add_argument('-r', '--route', dest='route_id', required=True, help="NJTransit bus route number")
parser.add_argument('-f', '--font', dest='font_type', choices=['text','font'], required=False, default='text', help='Use plain scrolling text or 2-line rendered fonts')
parser.add_argument('-z', '--zip', dest='zip', required=True, help="ZIPcode for weather")

# to do

# 2. fetch stop name and truncate (with manual label override also)
    #
# 3. length limit on bottom line to prevent errors
    # hunt down the original SF muni code
# 4. add a second stop and rotate every n seconds
    # strategy to parse arbitrary series of stop, route pairs
    # https://stackoverflow.com/questions/27146262/create-variable-key-value-pairs-with-argparse-python


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

#
# new architecture will need to loop the URL fetch for each stop + route combination
# which have to be specified in unique, explicit pairs
# e.g. -s 31031 119 -s 31031 85 -s 31285 87
#


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
# 8:28am Webster & Congress
# 119 3m 6m 19m 85 24m
#

# weather
temp_now = get_weather.temp(args.zip)

line2 = ''
bus_format = '%s min '

#
# REFACTOR THIS TO LOOP OVER ALL THE LINES FOR A SINGLE STOP WITH NO LINE DESIGNATED
#

for bus in arrivals:
    print bus
    if ';' in bus['pt']: # fix for response of APPROACHING e.g. 0 mins prediction
        bus['pt'] = '0!'
    bus_entry = bus_format % (bus['pt'])
    line2 = line2 + bus_entry
line2 = "#" + args.route_id + ' ' + line2
ogm = []
lines = []
line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) + ' ' + temp_now
lines.append(line1)
lines.append(line2)
ogm = lines[:2]
effect = 'hold'
speed=1

# send to LED
#handle differently depending on render method

try:
    if (args.write == True) and (args.font_type == 'font'):        
        WriteFont(ogm,effect,speed)
        print 'i tried WriteFont with'
        print ogm

    elif (args.write == True) and (args.font_type == 'text'):        
        effect = 'hold'
        WriteText(ogm,effect,speed)
        print 'i tried WriteText with'
        print ogm

except:
    pass

