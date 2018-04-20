# LED screen bus arrival display
# scrapes and parses NJT MyBusNow API XML to brightLEDsigns.com display
# single stop, single route for now

import urllib2, argparse, os, sys
from datetime import datetime   
import xml.etree.ElementTree
from weather import get_weather
from pyledsign.minisign import MiniSign
from simplefont import sign_font
import os, time

def serialfind():
    import platform, os, re
    platform_name = platform.system()
    tty = ''
    if platform_name == 'Linux':
        tty = '/dev/ttyUSB0'
    if platform_name == 'Darwin':
        dev_contents = os.listdir('/dev')
        for line in dev_contents:
            if "Repleo" in line:
                tty = ('/dev/' + str(line))
            elif 'tty.usbserial' in line:
                tty = '/dev/tty.usbserial'
            else:
                tty = '/dev/null'
    return

def WriteFont(lines, effect, speed):

    # prepare the bitmap
    class Array:
        def zero_one(self, data):
            zero_oned = ""
            for row in data:
                joined_row = "".join("{0}".format(n) for n in row)
                zero_oned += joined_row
            return zero_oned

    # font setup
    pwd = os.path.dirname(os.path.realpath(__file__))
    new_glyphs_path = '/'.join([pwd, 'fonts'])
    font = sign_font(new_glyphs_path)

    # sign setup
    portname = serialfind.serialfind()
    sign = MiniSign(devicetype='sign', port=portname, )

    # THIS IS BREAKING WHEN THE TEXT IS TOO LONG
    # render message as bitmap
    matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
    if not matrix:
        return False
    text_for_sign = Array().zero_one(matrix)
    typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);

    # queue and send message
    sign.queuemsg(data="%s" % typeset, effect='hold');
    sign.sendqueue(device=portname)
    time.sleep(6)

# parse services and switches
parser = argparse.ArgumentParser()
parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
parser.add_argument('-f', '--font', dest='font_type', choices=['text','font'], required=False, default='text', help='Use plain scrolling text or 2-line rendered fonts')
parser.add_argument('-z', '--zip', dest='zip', help="ZIP code of stop, for weather")

args = parser.parse_args()

# extract the service specs
n=0
service_specs=[]
for service in args.services:
    n=n+1
    stop_id=service.split(",")[0]
    route_id=service.split(",")[1]
    service_specs.append([n,stop_id,route_id])
    # print "service %s is stop %s route %s" % (n,stop_id,route_id)


#slideshow is a list of lists
# [ [slide1 line1, slide1,line2],
#   [slide2 line1, slide2,line2],
#   [slide3 line1, slide3,line2],
slideshow=[]


# FETCH arrival_list OVER EACH SERVICE service TO BUILD A slide AND APPEND TO slideshow
for service in service_specs:
    # create the url
    api_key = '0.3003391435305782'
    arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
    submit_url = arrivals_url % (service[2], service[1], api_key)
    # print submit_url

    try:
        data = urllib2.urlopen(submit_url).read()
    except urllib2.HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        sys.exit('Exiting.')
    except urllib2.URLError, e:
        print 'We failed to reach a server. (internet down?)'
        ogm = []
        ogm.append('offline')
        WritePlaintext(ogm,'hold',3)
        # print 'Reason: ', e.reason

        sys.exit('Exiting.')
    else:
        pass

    arrival_list = []

    e = xml.etree.ElementTree.fromstring(data)
    for atype in e.findall('pre'):
        fields = { }
        for field in atype.getchildren():
            if field.tag not in fields and hasattr(field, 'text'):
                if field.text is None:
                    fields[field.tag] = ''
                    continue
                fields[field.tag] = field.text.replace("&nbsp", "")

        arrival_list.append(fields)

    line2 = ''
    bus_format = '%s min'

    for bus in arrival_list:
        # print bus
        if ';' in bus['pt']: # handle response of APPROACHING e.g. 0 mins prediction
            bus['pt'] = '!0!'
        bus_entry = bus_format % (bus['pt'])s
        line2 = line2 + ' ' + bus_entry
    line2 = "#" + bus['rd'] + line2
    ogm = []
    lines = []
    # weather
    # temp_now = get_weather(args.zip)
    # line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) + '  ' + temp_now
    line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P'))
    lines.append(line1)
    lines.append(line2)
    slide = lines[:2]
    slideshow.append(slide)

print
print
print slideshow

sys.exit()




"""



    effect = 'hold'
    speed=1






#
# SEND ALL MESSAGES in QUEUE

#
# ROTATE: TELL THE SCREEN TO SWITCH MESSAGES (60/n sec each)


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------

#
# fetching and parsing data
# right now shows all buses for a single stop
# direction is implicit






# route_id = 'all'
# if args.route_id > 0:
#    route_id = args.route_id




# send to LED
#handle differently depending on render method

try:
    if (args.write == True) and (args.font_type == 'font'):        
        WriteFont(ogm,effect,speed)
        print 'i tried WriteFont with'
        print ogm

    elif (args.write == True) and (args.font_type == 'text'):        
        effect = 'hold'
        WriteText(ogm,effect,speed)
        print 'i tried WriteText with'
        print ogm

except:
    pass


"""