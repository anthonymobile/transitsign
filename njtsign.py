# LED screen bus arrival display
# scrapes and parses NJT MyBusNow API XML to brightLEDsigns.com display

import urllib2, argparse, os, sys
from datetime import datetime   
import xml.etree.ElementTree
from weather import get_weather
from pyledsign.minisign import MiniSign
from simplefont import sign_font
import os, time


def writesign(lines):

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
    portname = '/dev/ttyUSB0'
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
    sign.sendqueue(device=portname, runslots='none')


def main():

    # parse services and switches
    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    # extract the service specs
    n=0
    service_specs=[]
    for service in args.services:
        n=n+1
        stop_id=service.split(",")[0]
        route_id=service.split(",")[1]
        service_specs.append([n,stop_id,route_id])
        print "service %s is stop %s route %s" % (n,stop_id,route_id)

    # get arrivals for each service and parse
    slideshow=[]
    for service in service_specs:
        # create the url
        api_key = '0.3003391435305782'
        arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
        submit_url = arrivals_url % (service[2], service[1], api_key)
        print submit_url

        try:
            data = urllib2.urlopen(submit_url).read()
        except urllib2.HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            sys.exit('Exiting.')
        except urllib2.URLError, e:
            print 'We failed to reach a server. (internet down?)'
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

        # create slideshow
        line2 = ''
        bus_format = '%s min'
        for bus in arrival_list:
            if bool(bus) is True: # make sure there are predictions
                if ';' in bus['pt']:  # handle response of APPROACHING e.g. 0 mins prediction
                    bus['pt'] = '!0!'
                bus_entry = bus_format % (bus['pt'])
                line2 = line2 + ' ' + bus_entry # append the arrival time for each bus e.g. '22 min'
            else:
                line2 = 'No arrivals next 30 mins.'
            degree_sign= u'\N{DEGREE SIGN}'
            temp_now = get_weather('Jersey City') # hardcoded for now
            temp_msg = (temp_now['temp']+degree_sign)
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P'))+ ' ' + temp_msg
            lines = []
            lines.append(line1)
            lines.append('#' + bus['rd'] + line2)
            print lines
            slide = lines[:2]
            slideshow.append(slide)

    # removes duplicate slides created by above loop if multiple arriving buses
    # very kludgy need to fix
    if len(slideshow)>1:
        slideshow=slideshow[-1]
    print slideshow
    sys.exit()

    # manually cycle through each message, queue and send it
    num_slides = len(slideshow)  # type: int
    slide_duration = 60 / num_slides
    if args.write is True:
        print 'Writing to sign...'
        slidenum=0
        for slide in slideshow:
            print str(slidenum) + ': ',
            print slide
            writesign(slide)
            time.sleep(slide_duration)
    else:
        pass


if __name__ == "__main__":
    main()
