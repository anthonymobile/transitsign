import argparse

from Service import *
from Slide import *


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('services', nargs='+', help='Services specified as bus stop#,route# separated by comma with no space')
    parser.add_argument('-w', '--write', dest='write', action='store_true', help="Write the outgoing message (OGM) to the LED screen")
    args = parser.parse_args()

    # 1 create Service instances for each one passed
    for svc in args.services:
        stop_id = svc.split(",")[0]
        route_id = svc.split(",")[1]
        x = Service(svc)
        x.get_Arrivals.
        x._weather
        print "service: stop %s route %s" % (n, stop_id, route_id)
        # these should come back full of the arrival predictions

    # 2 make the slide and bitmaps
        Slide.compose_lines(x)
        # this comes back as a list of two strings
        Slide.typeset(x)
        # this comes back as a bitmap

    # 3 loop manually
    for slide in slideshow
        Slide.writesign(slide)

        num_slides = len(slideshow)  # type: int
        slide_duration = 60 / num_slides
        if args.write is True:
            print 'Writing to sign...'
            slidenum = 0
            for slide in slideshow:
                print str(slidenum) + ': ',
                print slide
                writesign(slide)
                time.sleep(slide_duration)
        else:
            pass


if __name__ == "__main__":
    main()
