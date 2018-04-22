# NJTsign v2.01
May 2018 
Anthony Townsend (anthony@bitsandatoms.net)

#### Object Oriented Version of earlier code


## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable.

## Classes

## Usage

```
TBD
```

## Dependencies

**pyserial**
This is the main one. 

**pyledsign**
I've bundled this code into the project since its stable for 2 years now. https://github.com/BrightLedSigns/pyledsign

**pyown**
For talking to open weather.

## NJT Bus Arrival Feeds

#### mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

#### API endpoint for the arrivals
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782
