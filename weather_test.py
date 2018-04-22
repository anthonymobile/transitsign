# weather_test
import argparse
from weather import get_weather

# parser = argparse.ArgumentParser()
# parser.add_argument('-z', '--zip', required='True', dest='zip', help="ZIP code of stop, for weather")
# args = parser.parse_args()


degree_sign= u'\N{DEGREE SIGN}'
#theweather= get_weather(args.zip)
theweather= get_weather('Jersey City')
print (theweather['temp']+degree_sign)
print (theweather['temp_lo']+degree_sign)
print (theweather['temp_hi']+degree_sign)
print (theweather['status'])