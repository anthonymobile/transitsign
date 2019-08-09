import argparse
import os
import time

from Service import Service
import urllib.request
import json
from pyledsign.minisign import MiniSign
from fonts.FontSimple import sign_font

# font setup
pwd = os.path.dirname(os.path.realpath(__file__))
new_glyphs_path = '../'.join(['fonts'])
font = sign_font(new_glyphs_path)


class Array:
    def zero_one(self, data):
        zero_oned = ""
        for row in data:
            joined_row = "".join("{0}".format(n) for n in row)
            zero_oned += joined_row
        return zero_oned


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    parser.add_argument('-c', '--controller', dest='controller_url', required=False, help="URL for config API e.g. http://buswatcher.code4jc.org/api/v1/sign?id=1&key=a7e6b3")
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    slideshow=[]

    # future fetch config from a remote controller
    # if args.controller == True:
    #     try:
    #         with urllib.request.urlopen(args.controller_url) as url:
    #             services = json.loads(url.read().decode())
    #
    #     sample response
    #
    #     {
    #         "services": [
    #             {
    #                 "route_id": "119",
    #                 "stop_id": "30189"
    #             },
    #             {
    #                 "route_id": "87",
    #                 "stop_id": "21062"
    #             }
    #         ]
    #     }
    # else:

    services_list = []
    for svc in args.services:
        insert=dict()
        insert['route_id']=svc.split(",")[1]
        insert['stop_id']=svc.split(",")[0]
        services_list.append(insert)
    services_dict=dict()
    services_dict['services']=services_list
    services = json.dumps(services_dict)


    # create the sign
    portname = '/dev/ttyUSB0'
    sign = MiniSign(devicetype='sign', port=portname, )

    # fetch the arrival predictions and format sign message text
    services_json = json.loads(services)
    for service in services_json['services']:

        svc = Service(service['stop_id'],service['route_id'])
        print("service: stop {a} route {b}".format(a=svc.stop, b=svc.route))
        print ("slide text: {text}".format(text=svc.slide_text))

        slideshow.append(svc.slide_text)

    # render and write to sign
    if args.write is True:
        num_slides = len(slideshow)  # type: int
        slide_duration = 60 / num_slides
        print ('Writing to sign...')


        # HOME VERSION
        # uses a single slide with first and second services on the lines
        slide = []
        for s in slideshow:
            slide.append(s[1])

        #todo figure out how to add the time to the right hand side if there is room w/0 truncating
        # maybe try to render it and except width > 96 and then render it without

        # render message as bitmap
        matrix = font.render_multiline(slide, 16 / 2, {"ignore_shift_h": True, "fixed_width": 96})
        if not matrix:
            return False
        text_to_set = Array().zero_one(matrix)
        typeset_slide = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_to_set)
        sign.queuemsg(data="%s" % typeset_slide, effect='hold');
        # queue and send message
        sign.sendqueue(device=portname, runslots='none')
        time.sleep(slide_duration)


if __name__ == "__main__":
    main()

