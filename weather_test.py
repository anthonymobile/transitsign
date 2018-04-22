# weather_test
import argparse
from weather import get_weather

parser = argparse.ArgumentParser()
parser.add_argument('-z', '--zip', required='True', dest='zip', help="ZIP code of stop, for weather")
args = parser.parse_args()


degree_sign= u'\N{DEGREE SIGN}'
temp_now = get_weather(args.zip)
print (temp_now['temp']+degree_sign)