# NJTsign v0.1
April 2018 
Anthony Townsend (anthony@bitsandatoms.net)

## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable.

## Usage

```
njtsign.py {stop_id,route_id,...} [-h] [-w] [-f {text,font}]


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

```sudo apt-get install python-serial```

**pyledsign**

```
git clone git@github.com:BrightLedSigns/pyledsign.git
cd pyledsign; python setup.py install
```

## NJT Bus Arrival Feed

### mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

###API endpoint for the arrivals
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782

###API with direction (untested) 
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782

