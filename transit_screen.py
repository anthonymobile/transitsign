# simplifed LED screen bus arrival display
# scapes and parses NJT MyBusNow XML to brightLEDsigns.com display
# Dec 2016 Anthony Townsend anthony@code4jc.org

# mobile website http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on
# API endpoint for the arrivals = XML of arrival predictions
# http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782
# n.b. see http://stackoverflow.com/questions/31754456/efficient-web-page-scraping-with-python-requests-beautifulsoup

# for testing: stop 30189 / routes 119 and 85 / direction 0 
# NJ.Jersey City.Congress+Webster / to NYC+Hoboken

import urllib2, args, os, sys, datetime
import xml.etree.ElementTree
from sign_writer import OGM_Write, OGM_Write_Badge

arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'

# with direction? (untested)
# http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782

now  = datetime.datetime.now()

# defaults
route_id='all'
key='0.3003391435305782'

# args w/ optional overrides
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--stop', dest='stop_id', required=True, help='NJTransit bus stop number')
parser.add_argument('-r', '--route', dest='route_id', default='---', required=False, help='NJTransit bus route number')
args = parser.parse_args()

ADD ARGS - write (testing, confirm write out)
ADD ARGS - screen or badge display


# some functions

# construct the request url
def make_url (stop_id, route_id, key):

	return submit_url =  stop_id, route_id, key

# get the data
def fetch_url (submit_url):

	return buses = urllib2.urlopen(submit_url)

# parse it
def parse_arrivals:

    data = urllib2.urlopen(_sources[source]).read()

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


# format for display
def format_lines (arrival_table):


	'''fields of interest
	<rn>128</rn> Route number
	<fd>168 PARAMUS FARVIEW AVE</fd> Final destination
	<pt>6</pt> Prediction time
	<pu>MINUTES</pu> Prediction units
	'''

	return ogm

# show it on the screen (grab the LED display code basefrom github)
def show_buses (ogm):

	speed=3
	effect='hold'

	try:
		if args.write == True:
			if args.xled == 'sign':
				from transit_functions import OGM_Write
				OGM_Write(args.platform,ogm,effect,speed)
				print 'Wrote to LED sign. Verify content.'
			elif args.xled == 'badge':
				from transit_functions import OGM_Write_Badge
				OGM_Write_Badge(args.platform,ogm,effect,speed)
				print 'Wrote to LED badge. Verify content.'
		else:
			print 'Write (-w) flag not set, not sending to LED.'

	except:
		print 'Error writing to sign. Are you sure its connected? Really are you sure?'


	return

# main program

make_url(arrivals_url, route_id, dir_id, stop_id, showAllBusses, findstop)

fetch_url(submit_url)

parse_arrivals(buses)

format_lines(arrivals)

show_buses(ogm)

