from template import template

class test_listener(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     '_listener_',
                        'description': 'Test listener',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['command',  'test module listening on channel'],
                    ]
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        content = ' '.join(buffparts[2:])
        if '?' in content:
            self.send('PRIVMSG {0} :yes..'.format(sendto))
