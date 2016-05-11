from template import template

import logging
from prettytable import PrettyTable

class dump(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'dump',
                        'description': 'List of CTF dump (binaries etc..)',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['',     'list of CTF dump (binaries etc..)'],
                    ]
        self.dump = [
                            {
                                'link':            'http://captf.com',
                            },
                            {
                                'link':            'http://shell-storm.org/repo/CTF',
                            },
                            {
                                'link':            'https://ctftime.org/writeups',
                            },
                        ]

    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        
        # prepare table columns
        t = PrettyTable(['link'])
        # table styling
        t.header_style = 'upper'
        t.border = True
        t.padding_width = 1
        t.sortby = 'link'
        t.align['link'] = 'l'
        # fill rows
        for link in self.dump:
            t.add_row([link['link']])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

        return
