# NJTsign
Dec 2016 
Anthony Townsend anthony@code4jc.org

## Description

A Python app to grab real-time bus arrival predictions from NJTransit.com BusTime app and push them to a brightledsigns.com display via USB serial cable.

## Dependencies

**pyledsign**

'''
git clone git@github.com:BrightLedSigns/pyledsign.git
cd pyledsign; python setup.py install
'''

## Notes on the Bus Arrival Feed

### mobile website
http://mybusnow.njtransit.com/bustime/eta/eta.jsp?route=---&direction=---&stop=---&id=30189&showAllBusses=on&findstop=on

###API endpoint for the arrivals
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=all&stop=30189&key=0.3003391435305782

###API with direction (untested) 
http://mybusnow.njtransit.com/bustime/eta/getStopPredictionsETA.jsp?route=%s&direction=%s&stop=%s&key=0.3003391435305782


## Step-By-Step Instructions to Configure on A Raspeberry Pi B / Zero

This might work on a Pi 2, I dont have one so I don't know. Almost certainly works on a 3.

10. Get the headless installer and start it.

'''
mkdir pi_install
cd pi_install
git clone git@github.com:containerstack/rpi-arch-builder.git
cd rpi-arch-builder
sudo ./installer.sh
'''

20. Work through the installer.

To figure out which disk:

'''
ls /dev/sd*
'''

30. Boot and Configure 

Install the microSD in a Pi and login as default user and change user and root passwords.

'''
ssh alarm@alarm
passwd
alarm
*type a newpassword*
*retype a newpassword*
su
root
passwd
*type a newpassword*
*retype a newpassword*
'''


40. Update Arch Linux and install required s/w

'''sudo pacman -Syu sudo ddclient python2 python2-setuptools python2-numpy python2-pyserial perl cronie base-devel python2-pyserial dosfstools wget git'''


45. mosh (OPTIONAL)

Mosh is very useful with these devices as you want a robust shell that can handle disconnections 

Setup locales:

uncomment #en_US.UTF-8 locale in /etc/locale.gen
'''nano /etc/locale.gen'''

Generate locales and keys
'''timedatectl set-timezone America/New_York
locale-gen
localectl set-locale LANG=en_US.UTF-8'''

Install mosh
'''pacman -Syu mosh
exit # (back to user account)
ssh-keygen -q -N "" -t rsa
'''

Logout and logback in 
'''logout
mosh alarm@host
''

50. Configure Sudo for user:alarm

'''export VISUAL=nano
visudo'''

Search for the section and add alarm as a fully-authorized sudoer:

'''
##
## User privilege specification
##
root ALL=(ALL) ALL
alarm ALL=(ALL) ALL
'''

**Everything from here on out is done as user alarm, not root.**


60. Get Application Code

'''cd ~
git clone https://github.com/anthonymobile/njtsign.git
git clone https://github.com/BrightLedSigns/pyledsign.git
cd pyledsign
python2 setup.py install
'''

70. Test the script

Try this:

'''/usr/bin/python2 /home/alarm/njtsign/njtsign.py -s 20496 -d badge -w'''


80. Setup Automation

Enable cron

'''sudo systemctl start cronie
sudo systemctl enable cronie'''

------------------------------------------------------------------
STOPPED HERE 26 DEC 2016
------------------------------------------------------------------

Setup the cron jobs

'''
export VISUAL=nano
crontab -e
'''

Example for LED sign (Hoboken Terminal):
'''
* * * * * /usr/bin/python2 /home/alarm/njtsign/njtsign.py -s 20496 -d badge -w
'''

Example for LED badge (Congress St and Webster Ave, Jersey City):
'''
* * * * * /usr/bin/python2 /home/alarm/njtsign/njtsign.py -s 30189 -d badge -w
'''
