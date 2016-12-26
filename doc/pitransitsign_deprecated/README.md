# branch = main

## test commands

simple, service 1  HBLR 2nd St southbound, service 2  HBLR 2nd St northbound

rm 20*;c;python transit.py -s1 rail 4 38441 1 -s2 rail 4 38441 0 -m schedule -x old -l 2 -w -p osx

## work log

### to do: general

1. migrate from submodules to dependencies, and point at original branches not my forks of pyledsign, pygtfs

### to do:  schedule-db-tweaks

1. abstract out NJ so it will take any gtfs file as an input (maybe use a feed source name as param and have the encoded in config file) - - this should mean the sqlite file can be removed from the repo (the script will fetcho n first run) look at Alex's buses.py for inspiration
2. add daily check for schedule update from transit.land and gtfs2db overwrite to update the local file 

### to do:  sign-refactor

1. test and debug OGM_Write_New with big screen (DONE)
2. deprecate OGM_Write_Old (DONE)
3. add -badge option to OGM_New (passed parameter = badge or sign, then used in the Sign class constructor)

### to do: major refactor using additional slots

1. can use other slots with ?

~~~~
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
~~~~

