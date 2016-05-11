from template import template

import logging
from prettytable import PrettyTable

class wargames(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'wargames',
                        'description': 'List of online wargames',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['',     'list online wargames'],
                    ]
        self.wargames = [
                            {
                                'name':            'OverTheWire: Wargames',
                                'link':            'http://overthewire.org/wargames',
                            },
                            {
                                'name':            'SmashTheStack: Wargaming Network',
                                'link':            'http://smashthestack.org/wargames',
                            },
                            {
                                'name':            'pwnable.kr',
                                'link':            'http://pwnable.kr',
                            },
                        ]

    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        # prepare table columns
        t = PrettyTable(['name', 'link'])
        # table styling
        t.header_style = 'upper'
        t.border = True
        t.padding_width = 1
        t.sortby = 'link'
        t.align['name'] = 'l'
        t.align['link'] = 'l'
        # fill rows
        for wargame in self.wargames:
            t.add_row([wargame['name'], wargame['link']])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

        return
