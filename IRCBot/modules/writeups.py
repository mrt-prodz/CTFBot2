from template import template

import logging
from prettytable import PrettyTable

class writeups(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'writeups',
                        'description': 'List of CTF writeups',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['',     'list of CTF writeups'],
                    ]
        self.writeups = [
                            {
                                'description':     'CTFTime writeups',
                                'link':            'https://ctftime.org/writeups',
                            },
                            {
                                'description':     'Large repositories of writeups',
                                'link':            'https://github.com/ctfs/write-ups',
                            },
                            {
                                'description':     'Collection of DEF CON CTF writeups',
                                'link':            'http://defcon.org/html/links/dc-ctf.html',
                            },
                        ]

    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        # prepare table columns
        t = PrettyTable(['link', 'description'])
        # table styling
        t.header_style = 'upper'
        t.border = True
        t.padding_width = 1
        t.sortby = 'link'
        t.align['link'] = 'l'
        t.align['description'] = 'l'
        # fill rows
        for writeup in self.writeups:
            t.add_row([writeup['link'], writeup['description']])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

        return
