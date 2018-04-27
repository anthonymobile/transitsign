# multi services not working

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

    class Array:
        def zero_one(self, data):
            zero_oned = ""
            for row in data:
                joined_row = "".join("{0}".format(n) for n in row)
                zero_oned += joined_row
            return zero_oned

    pwd = os.path.dirname(os.path.realpath(__file__))
    new_glyphs_path = '/'.join([pwd, 'fonts'])
    font = sign_font(new_glyphs_path)

    portname = '/dev/ttyUSB0'
    sign = MiniSign(devicetype='sign', port=portname, )

    # ------------------------------------------------------------------
    # THIS IS BREAKING WHEN THE TEXT IS TOO LONG
    # render message as bitmap
    matrix = font.render_multiline(lines, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
    if not matrix:
        return False
    text_for_sign = Array().zero_one(matrix)
    typeset = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_for_sign);
    # 
    # ------------------------------------------------------------------

    sign.queuemsg(data="%s" % typeset, effect='hold');
    sign.sendqueue(device=portname, runslots='none')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    n=0
    service_specs=[]
    for service in args.services:
        n=n+1
        stop_id=service.split(",")[0]
        route_id=service.split(",")[1]
        service_specs.append([n,stop_id,route_id])
        # print "service %s is stop %s route %s" % (n,stop_id,route_id)

    slideshow=[]
    for service in service_specs:
        api_key = '0.3003391435305782'
        arrivals_url = 'http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&stop=%s&key=%s'
        submit_url = arrivals_url % (service[2], service[1], api_key)

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

        line2 = ''
        bus_format = '%s min'
        if len(arrival_list)==0:
            line2 = 'No service.'
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P'))  # + ' ' + temp_msg
            lines = []
            lines.append(line1)
            lines.append('#' + service[2] + ' ' + line2)
            slide = lines[:2]
            slideshow.append(slide)
        else:
            for bus in arrival_list:
                if bool(bus) is True: 
                    if ';' in bus['pt']:  
                        bus['pt'] = '!0!'
                    bus_entry = bus_format % (bus['pt'])
                    line2 = line2 + ' ' + bus_entry 
            #degree_sign= u'\N{DEGREE SIGN}'
            #temp_now = get_weather('Jersey City') # hardcoded for now
            #temp_msg = (temp_now['temp']+degree_sign)
            line1 = datetime.now().strftime('%a') + ' ' + (datetime.now().strftime('%-I:%M %P')) # + ' ' + temp_msg
            lines = []
            lines.append(line1)
            lines.append('#' + bus['rd'] + line2)
            slide = lines[:2]
            slideshow.append(slide)
    # print slideshow


    num_slides = len(slideshow) 
    slide_duration = 60 / num_slides
    if args.write is True:
        # print 'Writing to sign...'
        for slot in range(len(slideshow)):
            print 'Slide ' + str(slot) + ': ',
            print slideshow[slot],
            writesign(slideshow[slot])
            print 'Sleeping for '+str(slide_duration)+' seconds...'
            time.sleep(slide_duration)


if __name__ == "__main__":
    main()
