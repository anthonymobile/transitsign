# NJTsign v0.2
April 2018 
Anthony Townsend (anthony@bitsandatoms.net)


![](https://github.com/anthonymobile/njtsign/blob/rotate_stops/IMG_0819.JPG)

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

## NJT Bus Arrival Feed

### mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

###API endpoint for the arrivals
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782

###API with direction (not yet used) 
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782
Since most stops only serve routes going in a single direction, not worried about this for a while.
