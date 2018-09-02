# NJTsign v2.01
May 2018 
Anthony Townsend (anthony@bitsandatoms.net)


## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable. Now fully object-oriented implementation.

## Hardware

Raspberry Pi (should run ok on a 0, 2 or 3 and a ['Mini' 16 by 96 pixel sign](https://brightledsigns.com/programmable/indoor/bs-4x16-mini) from BrightLedSigns.com. Update - BrightLedSigns is out of stock but points out that AliExpress still carries what appears to be [the same model](https://www.aliexpress.com/item/16x96Matrix-Led-desktop-display-red-color-LED-dot-matrix-signs-indoor-LED-moving-message-display-led/32522881975.html). We ordered one on 1 Sept 2018 for evaluation). Budget is about $150, including $90 for the sign and up to $60 for Pi, WiFi card and case.

![the hardware](doc/njtsign-hardware-v0.1.jpg)

## Classes

- Service
- Slide
- FontSimple

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
