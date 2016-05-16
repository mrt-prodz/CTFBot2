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

import threading, logging
from time import sleep
from IRCBot import IRCBot, settings

# ---------------------------------------------------------------------
# bot configuration: IRCBot/settings.py
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# logging settings
# ---------------------------------------------------------------------
logging.basicConfig(level=settings.loglevel, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

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
    for server in settings.config:
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
