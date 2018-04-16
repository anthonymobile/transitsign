# NJTsign v0.1
April 2018 
Anthony Townsend (anthony@bitsandatoms.net)

## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable.

## Usage

usage: njtsign.py [-h] [-w] -s STOP_ID

optional arguments:
  -h, --help            Show this help message and exit
  -w, --write           Write the outgoing message (OGM) to the LED screen
  -s STOP_ID, 			NJTransit bus stop number
  -r ROUTE_ID			NJTransit bus route number (if omitted=ALL)

## Dependencies

**pyserial**
'''sudo apt-get install python-serial'''

**pyledsign**
'''
git clone git@github.com:BrightLedSigns/pyledsign.git
cd pyledsign; python setup.py install
'''

## NJT Bus Arrival Feed

### mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

###API endpoint for the arrivals
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782

###API with direction (untested) 
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782


## Instructions

Recommended for Raspberry Pi Zero, 2 or 3.

1. Install required packages
TK sudo apt-get install pyserial

2. Get application code and dependcies

git clone https://github.com/anthonymobile/njtsign.git
git clone https://github.com/BrightLedSigns/pyledsign.git
cd pyledsign
python2 setup.py install
'''

3. Test the script

Try this:

'''/usr/bin/python njtsign/njtsign.py -s 20496'''

4. TK Setup Automation

Enable cron

'''sudo systemctl start cronie
sudo systemctl enable cronie'''


5. TK Setup

* * * * * cd /home/pi/njtsign && python2 njtsign.py -s 30189 -r 119 -w


