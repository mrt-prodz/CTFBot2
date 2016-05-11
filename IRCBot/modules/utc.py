from template import template

import pytz
from datetime import datetime

class utc(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'utc',
                        'description': 'Display current UTC time',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['command',  'display current UTC time'],
                    ]
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        
        self.send('PRIVMSG {0} :UTC time {1}'.format(sendto, datetime.now(pytz.utc).strftime("%H:%M")))
        return
