#!/bin/bash
# tunnel back to 3.crabdance.com
#  from http://www.tunnelsup.com/raspberry-pi-phoning-home-using-a-reverse-remote-ssh-tunnel
#
# setup instructions
# 1. as root: cp /root/pi_transitsign/misc/create_ssh_tunnel.sh /home/tunnel/create_ssh_tunnel.sh
# 2. crontab entry: * * * * * /usr/bin/bash /home/tunnel/create_ssh_tunnel.sh
#
# to initiate connection from 3.crabdance.com:
# ssh -l tunnel -p 2222 localhost


createTunnel() {
  /usr/bin/ssh -N -R 2222:localhost:22 tunnel@3.crabdance.com
  if [[ $? -eq 0 ]]; then
    echo Tunnel to 3.crabdance.com created successfully
  else
    echo An error occurred creating tunnel to 3.crabdance.com. RC was $?
  fi
}
/bin/pidof ssh
if [[ $? -ne 0 ]]; then
  echo Creating new tunnel connection
  createTunnel
fi
