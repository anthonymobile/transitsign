import argparse, sys

from lib.Service import Service
from lib.Slide import Slide
import json


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    # parser.add_argument('-f', '--forecast', dest='forecast', required=False, help="City, ST for weather forecast -OPTIONAL")
    parser.add_argument('-c', '--controller', dest='controller_url', required=False, help="URL for config API e.g. http://buswatcher.code4jc.org/api/v1/sign?id=1&key=a7e6b3")
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    slideshow=[]


    import urllib.request, json
    try:
        with urllib.request.urlopen(controller_url) as url:
            services = json.loads(url.read().decode())

    # sample response
    #
    # {
    #     "services": [
    #         {
    #             "route_id": "119",
    #             "stop_id": "30189"
    #         },
    #         {
    #             "route_id": "87",
    #             "stop_id": "21062"
    #         }
    #     ]
    # }


    except:
        services_list = []
        for svc in args.services:
            insert=dict()
            insert['route_id']=svc.split(",")[1]
            insert['stop_id']=svc.split(",")[0]
            services_list.append(insert)
        services_dict=dict()
        services_dict['services']=services_list
        services = json.dumps(services_dict)

    print(services)

    # now parse the json

    sjson = json.loads(services)
    for service in sjson['services']:

        svc = Service(service['stop_id'],service['route_id'])
        print (svc.stop)
        print("service: stop {a} route {b}".format(a=svc.stop, b=svc.route))

        arrival_data = svc.get_arrivals()
        slide_text = svc.compose_lines(arrival_data)
        print ("slide text: {text}".format(text=slide_text))

        this_slide = Slide()
        this_slide.typeset(slide_text)
        slideshow.append(this_slide)


    # now start sending the slideshow off to the sign with the sign class or function (or put that in Slide?)

    if args.write is True:

        slidenum = 0
        num_slides = len(slideshow)  # type: int
        slide_duration = 60 / num_slides

        print ('Writing to sign...')

        print (slideshow)

        for slide in slideshow:
            print (slide.typeset)
            print (str(slide) + ': ',)
            slide.writesign()
            time.sleep(slide_duration)

    else:
        pass

if __name__ == "__main__":
    main()

