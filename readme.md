# NJTsign v0.2
April 2018 
Anthony Townsend (anthony@bitsandatoms.net)


![](doc/njtsign-hardware-v0.1.jpg)

## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable.

## Usage

```
njtsign.py {stop_id1,route_id1} {stop_id2,route_id2} ... [-h] [-w] [-f {text,font}]


required arguments:
 STOP_ID,ROUTE_ID       service definition identified by NJTransit bus stop number and bus route number

 options
  -h, --help            show this help message and exit
  -w, --write           Write the outgoing message (OGM) to the LED screen
  -f {text,font}, --font {text,font}
                        Use plain scrolling text or 2-line rendered fonts
```

## Dependencies

**pyserial**
This is the main one. 

**pyledsign**
I've bundled this code into the project since its stable for 2 years now. https://github.com/BrightLedSigns/pyledsign

## Data Source

The app is powered by the prediction times on NJ Transit's Clever Devices API, which is the same service that all NJT's own apps and sites use. You can see the XML that comes back from the API for [arrivals](http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782).

## Automation

The program as coded only runs a single 1-minute loop. Ideally you want to run it every minute as a cron job. Here are some of the ways I use it near my intersection in Jersey City Heights, where my family uses multiple bus routes on a daily basis to get to various destinations.

```
# just 119
# * * * * * cd /home/pi/njtsign && python2 njtsign.py 30189,119 -w

# just webster ave 119 and 85
# * * * * * cd /home/pi/njtsign && python njtsign.py 30189,119 30189,85 -w

# 4 routes from the heights - nyc 119,123 hob term 85,87
# * * * * * cd /home/pi/njtsign && python njtsign.py 30189,119 21062,123 30189,$

# 119,85,119 and 87 - double cycle 119
# * * * * * cd /home/pi/njtsign && python njtsign.py 30189,119 30189,85 30189,1$

# fast cycle 10 seconds with focus on 119 -- 119,85,119,87,119,86P
* * * * * cd /home/pi/njtsign && python njtsign.py 30189,119 30189,85 30189,119 21062,87 30189,119 21065,86 -w
```
