from template import template

import logging
from prettytable import PrettyTable

class vulniso(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'vulniso',
                        'description': 'List of vulnerable ISO',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['',     'list vulnerable ISO'],
                    ]
        self.vulnisos = [
                            {
                                'name':            'PentesterLab',
                                'link':            'http://pentesterlab.com',
                            },
                            {
                                'name':            'Vulnhub',
                                'link':            'http://vulnhub.com',
                            },
                            {
                                'name':            'Metasploitable 2',
                                'link':            'http://sourceforge.net/projects/metasploitable',
                            },
                            {
                                'name':            'Exploit Exercises',
                                'link':            'http://exploit-exercises.com/download',
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
        t.sortby = 'name'
        t.align['name'] = 'l'
        t.align['link'] = 'l'
        # fill rows
        for vulniso in self.vulnisos:
            t.add_row([vulniso['name'], vulniso['link']])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))

        return
