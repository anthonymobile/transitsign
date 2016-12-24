import serialfind
from pyledsign.minisign import MiniSign

portname = serialfind('osx')

#!/usr/bin/python
from pyledsign.minisign import MiniSign
mysign = MiniSign(
    devicetype='sign',
)
# queue up a text message
mysign.queuemsg(
    data='Hello World'
)
# queue up a second message
#   - using the optional effect parameter.
#     if not supplied, defaults to 'scroll'
mysign.queuemsg(
    data='MSG 2',
    effect='snow'
)
#
# send the message to the sign via the serial port
#   note that the sendqueue() method does not empty
#   the buffer, so if we have a second sign, on a 
#   different serial port, we can send everything
#   to it as well...
#
mysign.sendqueue(
    device=portname
)
