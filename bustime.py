import argparse
import os
import sys

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
    parser.add_argument('-b', '--badge', dest='badge', action='store_true', help="Use badge")
    parser.add_argument('-r', '--rt_display', dest='rt_display', action='store_true', help="Surpress rute display")

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
    if args.badge == True:
        sign = MiniSign(devicetype='badge', port=portname, )
    elif args.badge == False:
        sign = MiniSign(devicetype='sign', port=portname, )

    # fetch the arrival predictions and format sign message text
    services_json = json.loads(services)
    for service in services_json['services']:

        svc = Service(service['stop_id'],service['route_id'],args.badge,args.rt_display)
        print("service: stop {a} route {b}".format(a=svc.stop, b=svc.route))

        if args.badge is True:
            print("slide text: {text}".format(text=svc.slide_text[1]))
        elif args.badge is False:
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


        # render message as bitmap

        if args.badge is True:
            width=48
            matrix = font.render(slide[0], 8, {"ignore_shift_h": True, "fixed_width": width})

            # # center the matrix with 2 rows above
            dummy_row = ([0] * width)
            matrix.insert(0, dummy_row)
            matrix.insert(0, dummy_row)

        elif args.badge is False:
            width=96
            matrix = font.render_multiline(slide, 16 / 2, {"ignore_shift_h": True, "fixed_width": width})
        if not matrix:
            return False

        for n in matrix:
            for c in n:
                if c == 1:
                    sys.stdout.write('*')
                else:
                    sys.stdout.write('-')
            print ()

        text_to_set = Array().zero_one(matrix)

        typeset_slide = sign.queuepix(height=len(matrix), width=len(matrix[0]), data=text_to_set)
        sign.queuemsg(data="%s" % typeset_slide, effect='hold');
        # queue and send message
        sign.sendqueue(device=portname, runslots='none')
        # time.sleep(slide_duration)


if __name__ == "__main__":
    main()

