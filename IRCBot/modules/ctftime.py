from template import template

import logging
import requests, time, json
from prettytable import PrettyTable
from datetime import datetime

class ctftime(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'ctftime',
                        'description': 'CTFTime calendar',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['list',     'list upcoming ctf'],
                        ['show #',   'show ctf info with id number #']
                    ]
        # api url
        self.api = 'https://ctftime.org/api/v1/'
        # excerpt of CTF name length
        self.namelimit = 24
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        if len(buffparts) >= 5:
        
            # list upcoming events (only ONLINE)
            if buffparts[4] == 'list':
                start = (int(datetime.now().strftime("%s")) * 1000) - 259200000
                finish = start + 2592000000
                req = requests.get(self.api + 'events/'
                                   + '?limit=10&start=' + str(start)
                                   + '&finish=' + str(finish))
                if req.status_code == 200:
                    try:
                        rss = req.text
                        #rss = rss.encode('utf8')
                        #rss = rss.encode('ascii', 'ignore')
                        ctfs = json.loads(rss)
                        # prepare table columns
                        t = PrettyTable(['id', 'title', 'start', 'finish'])
                        # table styling
                        t.header_style = 'upper'
                        t.border = True
                        t.padding_width = 1
                        t.align['id'] = 'r'
                        t.align['title'] = 'l'
                        t.align['start'] = 'l'
                        t.align['finish'] = 'l'
                        dateformat = '%Y-%m-%dT%H:%M:%S'
                        # fill rows
                        for index, ctf in enumerate(ctfs):
                            if ctf['format'] == 'Jeopardy':
                                name = ctf['title']
                                if len(name) > self.namelimit:
                                    name = name[0:self.namelimit] + '...'
                                start = datetime.strptime(ctf['start'][:-6], dateformat)
                                finish = datetime.strptime(ctf['finish'][:-6], dateformat)
                                ctfid = ctf['id']
                                now = datetime.now()
                                if (now >= start) and (now <= finish):
                                    ctfid = '[' + str(ctfid) + ']'
                                t.add_row([ctfid,
                                           name,
                                           start.strftime('%m/%d'),
                                           finish.strftime('%m/%d')])
                        # for each row send irc message
                        table = t.get_string().split('\n')
                        if len(table) > 0:
                            for line in table:
                                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

                    except Exception as error:
                        logging.error('ctftime parsing CTF error {0}'.format(error))
                else:
                    self.send('PRIVMSG {0} :[!] error while getting CTF list'.format(sendto))
                return

            # show specific event with ID
            if buffparts[4] == 'show':
                if len(buffparts) == 6:
                    req = requests.get(self.api + 'events/' + str(int(buffparts[5])) + '/')
                    if req.status_code == 200:
                        try:
                            rss = req.text
                            #rss = rss.encode('utf8')
                            #rss = rss.encode('ascii', 'ignore')
                            ctf = json.loads(rss)
                            
                            # prepare table columns
                            t = PrettyTable(['1','2'])
                            # table styling
                            t.border = True
                            t.header = False
                            t.padding_width = 1
                            t.align['1'] = 'r'
                            t.align['2'] = 'l'
                            # fill rows
                            dateformat = '%Y-%m-%dT%H:%M:%S'
                            start = datetime.strptime(ctf['start'][:-6], dateformat)
                            finish = datetime.strptime(ctf['finish'][:-6], dateformat)
                            t.add_row(['NAME',   '{1}'.format(sendto, ctf['title'])])
                            t.add_row(['START',  '{1}'.format(sendto, start)])
                            t.add_row(['FINISH', '{1}'.format(sendto, finish)])
                            t.add_row(['RATING', '{1}'.format(sendto, ctf['weight'])])
                            t.add_row(['FORMAT', '{1}'.format(sendto, ctf['format'])])
                            t.add_row(['URL',    '{1}'.format(sendto, ctf['url'])])
                            t.add_row(['',       '{1}'.format(sendto, ctf['ctftime_url'])])
                            # for each row send irc message
                            table = t.get_string().split('\n')
                            if len(table) > 0:
                                for line in table:
                                    self.send('PRIVMSG {0} :{1}'.format(sendto, line))

                        except Exception as error:
                            logging.error('ctftime parsing CTF error {0}'.format(error))
                    else:
                        self.send('PRIVMSG {0} :[!] no CTF found with this event ID'.format(sendto))
                    return

        # nothing to do here show help
        self._help_(sendto)
        return
        
