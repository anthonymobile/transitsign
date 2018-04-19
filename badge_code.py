# njtsign.py
#

parser.add_argument('-d', '--display', dest='display_type', default='sign', choices=['sign','badge'], required=True, help='brightLEDsigns.com display type')
args = parser.parse_args()


# LED DISPLAY 1 LINE AS PLAIN TEXT
def WriteText(lines, effect, speed):
    portname = '/dev/ttyUSB0'

    # setup sign
    mysign = MiniSign(devicetype='sign', )

    effect = 'scroll'

    # queue up a text message
    mysign.queuemsg(data=lines[0], effect=effect)

    # queue up a second message
    #   - using the optional effect parameter.
    #     if not supplied, defaults to 'scroll'
    mysign.queuemsg(data=lines[1], effect=effect)

    # send message
    mysign.sendqueue(device=portname)
    time.sleep(6)

