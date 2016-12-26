# transit_functions.py

import argparse, time, pickle, sys, datetime, os, warnings, urllib2
import pygtfs.pygtfs as gtfs
from ledsign.minisign import MiniSign
from operator import itemgetter
from sqlalchemy import exc as sa_exc

#--------------------------------------------------------
# benchmark speed decorator
def benchmark(func):
	def wrapper(*args, **kwargs):
		t = time.clock()
		res = func(*args, **kwargs)
		print ('execution time: ' + func.__name__, time.clock()-t)
		return res
	return wrapper

#--------------------------------------------------------
@benchmark
def StopsHandler(kind,route,stop,platform):

	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=sa_exc.SAWarning)
		
		# set working directories and db paths
		topdir='/root/pi_transitsign'
		if platform=='osx':
			topdir=os.getcwd()
		if kind=='rail':
			db =topdir+'/data/njt_rail.sqlite'
		elif kind=='bus':
			db =topdir+'/data/njt_bus.sqlite'

		# database and variables setup
		sched = gtfs.Schedule(db)
		stop_times=sched.stop_times
		trips=sched.trips
		stops=sched.stops
		# today=datetime.datetime.today()
		day_of_week=datetime.datetime.today().weekday()
		
		# loop over all stop_times
		stops_here_allday_temp = []
		for x in stop_times:
			# filter for stop number passed to function
			if int(x.stop_id) == stop:
				stop_add = {}
				stop_add['trip_id'] = x.trip_id
				stop_add['stop_id'] = x.stop_id
				stop_add['departure_time'] = x.departure_time
				stops_here_allday_temp.append(stop_add)

		# loop over all trips
		for y in stops_here_allday_temp:
			for z in trips:
				if z.trip_id == y['trip_id']:
					y['trip_headsign'] = z.trip_headsign.split(" ",1)[1]
					y['direction_id'] = z.direction_id
					y['service_id'] = z.service_id

		# match against correct service_id for that day
		stops_here_allday = []
		if day_of_week == 6:
			print 'its sunday!'
			stops_here_allday = [d for d in stops_here_allday_temp if d['service_id']=='12']

		elif day_of_week == 5:
			print 'its saturday!'
			stops_here_allday = [d for d in stops_here_allday_temp if d['service_id']=='13']

		elif day_of_week >= 4 or day_of_week <= 4:
			print 'its a weekday!'
			stops_here_allday = [d for d in stops_here_allday_temp if d['service_id']=='14']
		
		#
		# FUTURE		
		# to handle holidays, need to look at calendar_dates against 'service_id' for todays 'date'
		#

		# pickle it, write it out, return
		today=time.strftime("%Y%m%d")
		file_path='data/' + today + '_' + str(route) + '_' + str(stop) + '_stops.p'
		pickle.dump(stops_here_allday, open(file_path, "wb" ) )

		return

#--------------------------------------------------------
# @benchmark
def OGM_Create(stops_here,direction,lines,mode):

	# 1 sort the list of stops by departure time
	stops_sorted = sorted(stops_here, key=itemgetter('departure_time'))

	# print 'checking stops_sorted'
	# for x in range(10):
	#	print stops_sorted[x]

	# 2 filter out those that left already
	now = datetime.datetime.now()
	midnight = datetime.datetime.combine(now.date(), datetime.time())
	stops_soon = [s for s in stops_sorted if (midnight+s['departure_time'])>(now)]

	# 3 create time output field
	for i in stops_soon:
		# next line might need later for errors from late nights, DST, etc
		# i['time_output']= i['departure_time'].strftime("%Y-%m-%d %H:%M")
		i['departure_time']=midnight+i['departure_time']
		if mode=='schedule':
			i['time_output']= i['departure_time'].strftime("%-I:%M %p")
		elif mode=='countdown':
			i['time_output']  = str(int((i['departure_time']-now).total_seconds()/60))+' min'
	
		
	# 4 filter by direction
	#
	# print 'Direction is ' + str(direction)
	ogm_buffer = [s for s in stops_soon if s['direction_id']==direction]

	# 5 retain only the next 2 departures w/ Headsign and departure time
	ogm = []
	if lines==1:
		ogm.append(ogm_buffer[0]['trip_headsign'] + ' ' + ogm_buffer[0]['time_output'])
	elif lines==2:
		ogm.append(ogm_buffer[0]['trip_headsign'] + ' ' + ogm_buffer[0]['time_output'])
		ogm.append(ogm_buffer[1]['trip_headsign'] + ' ' + ogm_buffer[1]['time_output'])

	# print ogm
	return ogm

#--------------------------------------------------------
# @benchmark
def OGM_Write(platform,lines,effect,speed):
	
	# need later to format the ogm
	class Array:
		def zero_one(self, data):
			zero_oned = ""
			for row in data:
				joined_row = "".join("{0}".format(n) for n in row)
				zero_oned += joined_row
			return zero_oned

	# font setup
	from simplefont import sign_font
	pwd = os.path.dirname(os.path.realpath(__file__))
	new_glyphs_path = '/'.join([pwd,'glyphs'])
	
	# sign setup
	if platform == 'osx':
		portname = '/dev/tty.usbserial'
	else:
		portname ='/dev/ttyUSB0'
	sign = MiniSign(devicetype='sign', port=portname,)

	font = sign_font(new_glyphs_path)


	# sign screen_height hardcoded for now, better if it can be pulled from 
	# the MiniSign class instance 'sign'
	# e.g. sign.SCREEN_HEIGHT / 2, or some such
	# hardcoded for now original code below, again shoud be pulled ideally 
	# from the class instance
	# "fixed_width" : LEDSign.SCREEN_WIDTH
	matrix = font.render_multiline(lines, 16 / 2,{"ignore_shift_h" : True, "fixed_width" : 96})

	if not matrix:
		return False
	
	text_for_sign = Array().zero_one(matrix)
	typeset=sign.queuepix(height=len(matrix), width =len(matrix[0]), data  = text_for_sign);
	sign.queuemsg(data="%s" % typeset, effect=effect);
	sign.sendqueue(device=portname)

	time.sleep(6)

#--------------------------------------------------------
# should be able to deprecate this soon
# @benchmark
def OGM_Write_Badge(platform,line,effect,speed):

# can only be used with a 1-line service display

	if platform == 'osx':
		portname = '/dev/tty.usbserial'
	else:
		portname ='/dev/ttyUSB0'

	badge = MiniSign(devicetype='badge', port=portname)
	badge.queuemsg(data=line)
	badge.sendqueue(device=portname)

	time.sleep(6)


#--------------------------------------------------------
# @benchmark
def CheckRouteStop(platform,kind,route_id,stop_id):

	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=sa_exc.SAWarning)

		# set working directories and db paths
		topdir='/root/pi_transitsign'
		if platform=='osx':
			topdir=os.getcwd()
		if kind=='rail':
			db =topdir+'/data/njt_rail.sqlite'
		elif kind=='bus':
			db =topdir+'/data/njt_bus.sqlite'
		sched = gtfs.Schedule(db)
		routes=sched.routes
		stops=sched.stops
		print ('Checking request: Route ' + str(route_id) + ', Stop ' + str(stop_id))
		route_check = False
		stop_check = False
		for j in routes:
			if int(j.route_id) == int(route_id):
				route_check = True
				print 'Route valid.'
				break
		for k in stops:
			if int(k.stop_id) == int(stop_id):
				stop_check = True
				print 'Stop valid.'
				break
		if stop_check == False:
			sys.exit('Stop is invalid. Please re-check and try again.')
		if route_check == False:
			sys.exit('Route is invalid. Please re-check and try again.')
		return



