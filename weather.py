# weather.py

def get_weather (location):

	import pyowm

	owm = pyowm.OWM('d03e7d5526d81ddc4c1b4ec24a1915c9')  # You MUST provide a valid API key

	try:
		observation = owm.weather_at_place(location)
		w = observation.get_weather()
		temps = w.get_temperature(unit='fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

		report={}

		temp_str = "%.0f" % temps['temp']
		temphi_str = "%.0f" % temps['temp_max']
		templo_str = "%.0f" % temps['temp_min']

		report['temp'] = temp_str
		report['temp_hi'] = temphi_str
		report['temp_lo'] = templo_str
		status=str(w.get_status)
		report['status']=status.split('=')[2][:-2]

	except:
		print('Couldnt reach the weather API endpoint. Internet down?')
  
	return report



"""
import pyowm

owm = pyowm.OWM('PASTE YOUR API KEY IN HERE')  
observation = owm.weather_at_place("Cambridge,uk")  
w = observation.get_weather()  
wind = w.get_wind()  
print(w)  
print(wind) 
temperature = w.get_temperature('celsius')  
"""
