#========================================================
# transit.py 
# August 2016

import argparse, os, sys

#--------------------------------------------------------
# parse command line options

parser = argparse.ArgumentParser()

# services
# -s1 rail 4 38441 1 -s2 bus 4 38441 1
parser.add_argument('-s1','--service1', nargs='+', help='Service 1 (required): kind,route_id,stop_id,direction', required=True)
parser.add_argument('-s2','--service2', nargs='+', help='Service 1 (required): kind,route_id,stop_id,direction', required=False)

# other options
parser.add_argument("-m", "--mode", type=str, choices=['schedule', 'countdown'], help="time display mode(required)", required=True, default='schedule')
parser.add_argument("-x", "--xled", type=str, choices=['sign', 'badge'], help="LED screen driver", default='sign')
parser.add_argument("-l", "--lines", type=int, help="number of lines ['1 or 2, default=2']", default=2)
parser.add_argument("-w", "--write", dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
parser.add_argument("-p", "--platform", type=str, choices=['pi', 'osx'], help="platform(required)", required=True, default='pi')
args=parser.parse_args()

#--------------------------------------------------------
# concatenate service list

services=1
service_list=[]
service_list.append(args.service1)
if args.service2 is not None:
	services=2
	service_list.append(args.service2)

#--------------------------------------------------------
# create OGM component for each service

ogm_whole=[]

for s in service_list:

	# validate the request against GTFS schedule
	from transit_functions import CheckRouteStop
	CheckRouteStop(args.platform,s[0],s[1],s[2])

	# check to see if the database exists
	topdir='/root/pi_transitsign'
	if args.platform=='osx':
		topdir=os.getcwd()
	db_path_bus=topdir + '/data/njt_bus.sqlite'
	db_path_train=topdir + '/data/njt_rail.sqlite'

	if s[0] == 'rail':
		if os.path.isfile(db_path_train) == False:
			# TO DO - call db fetch and update routine
			# get_gtfsdata(source)
			import sys
			sys.exit('GTFS database not found. Exiting.')

	if s[0] == 'bus':
		if os.path.isfile(db_path_bus) == False:
			# TO DO - call db fetch and update routine
			# get_gtfsdata(source)
			import sys
			sys.exit('database not found. Exiting.')

	#--------------------------------------------------------
	# pickle file handler
	import time
	today=time.strftime("%Y%m%d")
	stops_here_allday=[]
	file_path='data/' + today + '_' + str(s[1]) + '_' + str(s[2]) + '_stops.p'
	
	import pickle

	if os.path.isfile(file_path):
		stops_here_allday=pickle.load(open(file_path, "rb" ) )

	else:

		#--------------------------------------------------------
		# make a lockfile and make the picklefile

		LOCKFILE_LOCATION = 'busy.LOCK'

		try:
			# write lockfile w/ pid
			lockfile = os.open(LOCKFILE_LOCATION, os.O_CREAT|os.O_WRONLY|os.O_EXCL)
			os.write(lockfile, str(os.getpid()))

		except OSError:
			# there already is a lockfile so we need to make sure some other process isn't making a pickle already
			print 'Theres a lock already...'
			import psutil

			process_table=[]
			for proc in psutil.process_iter():
				try:
					pinfo = proc.as_dict(attrs=['pid', 'name','cmdline'],ad_value='Ignore')
					process_table.append(pinfo)
				except psutil.NoSuchProcess:
					pass

			count = 0

			for proc in process_table:
				# concatenate the cmdline list back into a single string
				proc['cmdline'] = ' '.join(map(str, proc['cmdline']))
				# then search for transit.py
				if 'python2 transit.py' in proc['cmdline']:
					count = count + 1
					print str(proc['pid']) + '\t' + proc['cmdline']
			
			print 'Found ' + str(count) + ' transit.py instance(s).'

			if count > 1:
				print("Stopping this instance.")
				import sys
				sys.exit('Stopped.')
			else:
				os.remove(LOCKFILE_LOCATION)
				print("No other processes found. Deleting lockfile and proceeeding.")

		# now make the schedule picklefile
		print ("Making schedule picklefile...")
		from transit_functions import StopsHandler
		StopsHandler(s[0],int(s[1]),int(s[2]),args.platform)
		stops_here_allday=pickle.load(open(file_path, "rb" ) )

		# cleanup - Delete the lockfile
		os.remove(LOCKFILE_LOCATION)

	# create and format the OGM for this service
	from transit_functions import OGM_Create
	ogm_part=OGM_Create(stops_here_allday,int(s[3]),args.lines,args.mode)
	ogm_whole.append(ogm_part)


#--------------------------------------------------------
# assemble the final OGM across all services

ogm_final=[]

if args.lines == 1:
	# 1 line, 1 service
	if services == 1:
		ogm_final.append(ogm_whole[0][0])
		# train1
		# weather

	# 1 line, 2 service
	elif services == 2:
		ogm_final.append(ogm_whole[0][0] + ' ' + ogm_whole[1][0] + '... ')
		# svce1train1 svce2train1...
		# weather

elif args.lines == 2:
	print '*&*&*&'
	# 2 line, 1 service
	if services == 1:
		ogm_final.append(ogm_whole[0][0] + ' ' + ogm_whole[0][1] + '... ')
	# train1 train2...
	# weather

'''
	# 2 line, 2 service
	if services == 2:
		ogm_final.append(ogm_whole[0][0])
		ogm_final.append(ogm_whole[1][0])
		print 'ogm_final (list ok for 2-line) = '
		print ogm_final	
'''

#--------------------------------------------------------
# get the weather

from weather import get_weather
report=get_weather('hoboken,us')

line=str(report['status']+' '+report['temp']+'F '+'Hi '+report['temp_hi']+'F')
print line
ogm_final.append(line)

#--------------------------------------------------------
# report out

print '-sending to LED-------'
print ogm_final
print '----------------------'


#--------------------------------------------------------
# write to LED

speed=3
effect='hold'

try:
	if args.write == True:
		if args.xled == 'sign':
			from transit_functions import OGM_Write
			OGM_Write(args.platform,ogm_final,effect,speed)
			print 'Wrote to LED sign. Verify content.'
		elif args.xled == 'badge':
			from transit_functions import OGM_Write_Badge
			OGM_Write_Badge(args.platform,ogm_final,effect,speed)
			print 'Wrote to LED badge. Verify content.'
	else:
		print 'Write (-w) flag not set, not sending to LED.'

except:
	print 'Error writing to sign. Are you sure its connected? Really are you sure?'

