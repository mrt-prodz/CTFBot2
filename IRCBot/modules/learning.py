from template import template

import logging
from prettytable import PrettyTable

class learning(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'learning',
                        'description': 'List of learning materials',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['',     'list of learning materials'],
                    ]
        self.learning = [
                            {
                                'description':     'Large collection of url related to pentesting',
                                'link':            'http://code.google.com/p/pentest-bookmarks',
                            },
                            {
                                'description':     'PentesterLab bootcamp',
                                'link':            'https://pentesterlab.com/bootcamp',
                            },
                            {
                                'description':     'Open Web Application Security Project',
                                'link':            'https://owasp.org',
                            },
                            {
                                'description':     'Classes about reverse engineering',
                                'link':            'http://opensecuritytraining.info/Training.html',
                            },
                            {
                                'description':     'CTF field guide',
                                'link':            'http://trailofbits.github.io/ctf',
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
        for link in self.learning:
            t.add_row([link['link'], link['description']])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

        return
