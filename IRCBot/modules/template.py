# derive all modules from this class and override self.config, self.help, self._cmd_()
from prettytable import PrettyTable
class template(object):
    def __init__(self, send):
        self.send = send
        self.activated = True
        self.config = {
                        # module name (in case of collision it will be renamed from the bot)
                        'name':        self.__class__.__name__,
                        # trigger command (ex: !template) do not specify bot command trigger
                        'trigger':     'template',
                        # small description for the plugin
                        'description': 'Template module for IRCBot commands',
                        # privileges needed to run this module (guest|admin)
                        'allow':       'guest',
                    }
        self.help = [
                        # display module usage
                        ['','this module has no parameter']
                    ]
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        self.send('PRIVMSG {0} :[+] {1} test'.format(sendto, self.config['name']))

    def _help_(self, sendto):
        # prepare table columns
        t = PrettyTable(['1','2'])
        # table styling
        t.border = True
        t.header = False
        t.padding_width = 1
        t.align['1'] = 'l'
        t.align['2'] = 'l'
        # fill rows
        for line in self.help:
            t.add_row([line[0], line[1]])
        # for each row send irc message
        table = t.get_string().split('\n')
        if len(table) > 0:
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))
        """
        for line in self.help:
            self.send('PRIVMSG {0} :    {1}'.format(sendto, line))
        """