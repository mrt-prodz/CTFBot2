from template import template

import logging

class raw(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'raw',
                        'description': 'Send RAW commands',
                        'allow':       'admin',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['command',  'run RAW command'],
                    ]
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        
        # list upcoming events (only ONLINE)
        if len(buffparts) >= 4:
            self.send(' '.join(buffparts[4:]))
            return

        return
