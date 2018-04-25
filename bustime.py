import argparse

from Service import Service
#from Slide import Slide


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    # parser.add_argument('-f', '--forecast', dest='forecast', required=False, help="City, ST for weather forecast -OPTIONAL")
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    slideshow=[]

    # fetch arrivals and make slides for each requested service
    for svc in args.services:
        stop_id = svc.split(",")[0]
        route_id = svc.split(",")[1]
        print "service: stop %s route %s <<<< " % (stop_id, route_id),
        arrivals = Service(stop_id,route_id).get_arrivals()
        print arrivals
        slide_text = arrivals.compose_lines
        print "slide text: %s " % slide_text
        slide_type = Slide.typeset(slide_text)
        slideshow.append(slide_type)

    # now start sending the slideshow off to the sign with the sign class or function (or put that in Slide?)

    if args.write is True:

        slidenum = 0
        num_slides = len(slideshow)  # type: int
        slide_duration = 60 / num_slides

        print 'Writing to sign...'

        for slide in slideshow:
            print str(slidenum) + ': ',
            print slide
            slideshow[slidenum].writesign
            time.sleep(slide_duration)

    else:
        pass

if __name__ == "__main__":
    main()

