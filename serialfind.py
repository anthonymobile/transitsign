# sets the USB serial port ttyhandle
# default for linux is /dev/ttyUSB0
# for OSX, search for a Repleo driver handle
# otherwise default is /dev/tty.usbserial if it exists

def serialfind():

    import platform, os, re

    # 1 figure out platform
    platform_name = platform.system()
    tty =''

    if platform_name == 'Linux':
        tty = '/dev/ttyUSB0'

    if platform_name == 'Darwin':
        
        dev_contents = os.listdir('/dev')
        
        for line in dev_contents:
            if "Repleo" in line:
                tty = ('/dev/'+str(line))
            elif 'tty.usbserial' in line:
                tty = '/dev/tty.usbserial'
    else:
        tty='/dev/null'

    return tty
