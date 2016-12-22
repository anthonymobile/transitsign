# Dec 2016 Anthony Townsend anthony@code4jc.org


# requirements

## pyledsign
git clone git@github.com:BrightLedSigns/pyledsign.git
cd pyledsign; python setup.py install

## for OSX, prolific serial driver
http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=229&pcid=41

# notes on the bus arrival feed

## mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

##API endpoint for the arrivals = XML of arrival predictions
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782

##with direction? (untested) 
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782

n.b. see http://stackoverflow.com/questions/31754456/efficient-web-page-scraping-with-python-requests-beautifulsoup


##for testing: stop 30189 / routes 119 and 85 / direction 0 
NJ.Jersey City.Congress+Webster / to NYC+Hoboken