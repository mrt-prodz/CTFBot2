#!/usr/bin/env python
# -----------------------------------------------------------------------------
# CTFBot2 by Themistokle "mrt-prodz" Benetatos
# --------------------------------------------
# Small IRC bot listing upcoming CTF events from ctftime.org
# 
# Features: - upcoming CTFs from ctftime.org API
#           - can join multiple servers/channels
#           - small list of resources related to computer security
#
# ------------------------
# http://www.mrt-prodz.com
# https://github.com/mrt-prodz/CTFBot2
# -----------------------------------------------------------------------------

import threading, logging, os
from time import sleep
from IRCBot import IRCBot

# ---------------------------------------------------------------------
# bot configuration
# ---------------------------------------------------------------------
config = [
            {
                'host'    :'10.0.0.10',
                'port'    : 6697,
                'ssl'     : True,
                'nick'    : 'ctfbot',
                'chans'   : ['#ctfbot'],
                'pwd'     : 'nickservbotpassword',
                'salt'    : 'Salty Cheesy Poofs!',
                'admin'   : 'df9947089cd1895cce41cffb4dc8388ff11aa134b3f16d6587e306ed33882060',
                'enabled' : True,
            },
        ]

# on config where the user running this bot has no $HOME and rights to
# write in current folder set path to /tmp for example
os.environ['HOME'] = '/tmp'

# ---------------------------------------------------------------------
# logging settings
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# ---------------------------------------------------------------------
# clean exit of all threads
# ---------------------------------------------------------------------
def cleanexit(threads):
    logging.debug('user sent sigint.. terminating.')
    logging.debug('stopping threads.. please wait.')
    for t in threads:
        t.exitFlag = True
        t.disconnect()
        t.join()

# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------
if __name__ == '__main__':
    threads = []
    # run bot in threads
    for server in config:
        if server['enabled']:
            t = IRCBot(server)
            threads.append(t)
            t.daemon = True
            t.start()

    # reason of multiple try/catch is to properly get keyboard interrupt
    try:
        # loop until keyboard interrupt
        while True:
	    sleep(0.1)
            try:
                try:
                    threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
                except KeyboardInterrupt:
                    cleanexit(threads)
                    break
            except (KeyboardInterrupt, SystemExit):
                cleanexit(threads)
                break
    except KeyboardInterrupt:
        cleanexit(threads)
        
    # goodbye
    logging.debug('CTFBot ended.')
