import sys, threading, socket, ssl, time, logging, pkgutil, hashlib, importlib, os
from prettytable import PrettyTable

# ---------------------------------------------------------------------
# IRC bot class
# ---------------------------------------------------------------------
class IRCBot (threading.Thread):
    # ---------------------------------------------------------------------
    # bot configuration
    # ---------------------------------------------------------------------
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.trigger = '@'
        self.admin = ''
        self.salt = config['salt']
        self.password = config['admin']
        self.authed = False
        self.modules = {}
        self.host = config['host']
        self.port = config['port']
        self.ssl = config['ssl']
        self.nick = config['nick']
        self.nickpass = config['pwd']
        self.chans = config['chans']
        self.sbuffer = 4096
        self.irc = None
        self.exitFlag = False
        # make help table -> list
        self.helpObj = [
                            ['guest', 'help [module name]',    'display module help'],
                            ['guest', 'modules',               'display modules'],
                            ['admin', 'reload',                'reload modules and/or add new'],
                            ['admin', 'enable [module name]',  'enable module'],
                            ['admin', 'disable [module name]', 'disable module'],
                       ]
        # prepare table columns
        t = PrettyTable(['user', 'trigger', 'description'])
        # table styling
        t.header_style = 'upper'
        #t.border = False
        t.padding_width = 1
        t.sortby = 'user'
        t.align['user'] = 'l'
        t.align['trigger'] = 'l'
        t.align['description'] = 'l'
        for cmd in self.helpObj:
            t.add_row([cmd[0], self.trigger + cmd[1], cmd[2]])
        # for each row send irc message
        self.help = t.get_string().split('\n')

    # ---------------------------------------------------------------------
    # thread run, will keep reconnecting until exitFlag is set to True
    # ---------------------------------------------------------------------
    def run(self):
        # load bot modules
        self.loadmodules()
        # keep connecting until exit flag is true
        while not self.exitFlag:
            try:
                self.connect()
            except Exception as error:
                logging.error('error: {0}'.format(error))
            time.sleep(5)
        # clean disconnect
        self.disconnect()
        return

    # ---------------------------------------------------------------------
    # load modules and store into modules dictionnary
    # ---------------------------------------------------------------------
    def loadmodules(self):
        # remove stored modules
        self.modules.clear()
        modules = pkgutil.iter_modules(path=[os.path.dirname(__file__) + '/modules'])
        for loader, mod_name, ispkg in modules: 
            if mod_name == 'template':
                continue
            if mod_name not in sys.modules:
                # load module and store in modules
                logging.debug('loading module: {0}'.format(mod_name))
                try:
                    module = importlib.import_module('.{0}'.format(mod_name), 'IRCBot.modules')
                    # class name should be the same as file name
                    loaded_class = getattr(module, mod_name)
                    # init module with reference to send method
                    instance = loaded_class(self.send)
                    # if trigger already exists change it and add to modules
                    while instance.config['trigger'] in self.modules:
                        instance.config['trigger'] += '_'
                    # store module in modules dictionnary and use trigger as key
                    self.modules[instance.config['trigger']] = instance
                except Exception as error:
                    logging.error('error while loading modules: {0}'.format(error))
            else:
                logging.debug('module {0} already loaded, reloading'.format(mod_name))
                reload(mod_name)

    # ---------------------------------------------------------------------
    # connect to server
    # ---------------------------------------------------------------------
    def connect(self):
        logging.debug('connecting to {0}'.format(self.host))
        try:
            if self.ssl:
                ircc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ircc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.irc = ssl.wrap_socket(ircc)
            else:
                self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            logging.critical('cannot create socket: {0}'.format(error))
            return

        try:
            self.irc.connect((self.host, self.port))
        except socket.gaierror as error:
            logging.critical('cannot connect to {0} on port {1}: {2}'.format(self.host, self.port, error))
            return

        self.send('USER {0} {1} {2} :ctfbot'.format(self.nick, self.nick, self.nick))
        self.send('NICK {0}'.format(self.nick))
        self.loop()

    # ---------------------------------------------------------------------
    # disconnect from current server
    # ---------------------------------------------------------------------
    def disconnect(self):
        logging.debug('disconnecting from {0}'.format(self.host))
        try:
            logging.debug('disconnecting from {0}'.format(self.host))
            self.send('PRIVMSG {0} :[user sent sigint] terminating.'.format(self.chan))
            self.send('QUIT plop!')
            self.irc.shutdown(socket.SHUT_RDWR)
            self.irc.close()
        except socket.error as error:
            logging.critical('socket error: {0}'.format(error))

    # ---------------------------------------------------------------------
    # send message
    # ---------------------------------------------------------------------
    def send(self, cmd):
        self.irc.send(cmd + '\r\n')

    # ---------------------------------------------------------------------
    # return if user has been authorized or not
    # ---------------------------------------------------------------------
    def checkauth(self, user):
        if (self.authed) and (user == self.admin):
            return True
        return False
        
    # ---------------------------------------------------------------------
    # parsing commands sent from user
    # ---------------------------------------------------------------------
    def parsecmd(self, cmd, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        senderip = buffparts[0].split('@')[1]
        # send to channel by default
        sendto = buffparts[2]
        # if buffparts[2] is the botname send to user
        if (buffparts[2] == self.nick):
            sendto = buffparts[0].split('!')[0][1:]

        # ---------------------------------------------------------------------
        # show help
        # ---------------------------------------------------------------------
        if cmd == 'help':
            # if we have a 5th argument, show module help
            if len(buffparts) == 5:
                for module in self.modules:
                    if buffparts[4] == self.modules[module].config['name']:
                        self.modules[module]._help_(sendto)
            # else show bot help
            else:
                for line in self.help:
                    self.send('PRIVMSG {0} :{1}'.format(sendto, line))
            return
            
        # ---------------------------------------------------------------------
        # list modules
        # ---------------------------------------------------------------------
        if cmd == 'modules':
            # display guest modules
            # prepare table columns
            t = PrettyTable(['', 'module', 'trigger', 'description'])
            # table styling
            t.header_style = 'upper'
            t.border = True
            t.padding_width = 1
            t.sortby = 'module'
            t.align['module'] = 'l'
            t.align['trigger'] = 'l'
            t.align['description'] = 'l'

            # fill rows
            for mod in self.modules:
                module = self.modules[mod]
                # show guest modules
                if module.config['allow'].lower() == 'guest':
                    t.add_row(['[{0}]'.format(('+' if module.activated else ' ')), module.config['name'], self.trigger + module.config['trigger'], module.config['description']])

                # show admin modules
                elif self.checkauth(buffparts[0]):
                    t.add_row(['-[{0}]-'.format(('+' if module.activated else ' ')), module.config['name'], self.trigger + module.config['trigger'], module.config['description']])

            # for each row send irc message
            table = t.get_string().split('\n')
            for line in table:
                self.send('PRIVMSG {0} :{1}'.format(sendto, line))
                
            return

        # ---------------------------------------------------------------------
        # authorize user for admin commands access
        # ---------------------------------------------------------------------
        if cmd == 'auth':
            if len(buffparts) == 5:
                if self.password == hashlib.sha256(buffparts[4].encode()+self.salt.encode()).hexdigest():
                    self.send('PRIVMSG {0} :[+] access granted'.format(sendto))
                    self.admin = buffparts[0]
                    self.authed = True
                else:
                    self.authed = False
                return
        
        # ---------------------------------------------------------------------
        # commands for admin only
        # ---------------------------------------------------------------------
        if self.checkauth(buffparts[0]):
            # -----------------------------------------------------------------
            # reload modules during runtime (add new to the list as well)
            # -----------------------------------------------------------------
            if (cmd == 'reload'):
                self.send('PRIVMSG {0} :[+] reloading modules'.format(sendto))
                self.loadmodules()
                return
            # -----------------------------------------------------------------
            # disable module during runtime
            # -----------------------------------------------------------------
            if (cmd == 'disable'):
                if len(buffparts) == 5:
                    for module in self.modules:
                        if buffparts[4] == self.modules[module].config['name']:
                            # check if module is enabled
                            if self.modules[module].activated:
                                self.send('PRIVMSG {0} :[+] disabling module: {1}'.format(sendto, buffparts[4]))
                                self.modules[module].activated = False
                            else:
                                self.send('PRIVMSG {0} :[!] module {1} is already disabled'.format(sendto, buffparts[4]))
                return
            # -----------------------------------------------------------------
            # enable module during runtime
            # -----------------------------------------------------------------
            if (cmd == 'enable'):
                if len(buffparts) == 5:
                    for module in self.modules:
                        if buffparts[4] == self.modules[module].config['name']:
                            # check if module is already enabled
                            if self.modules[module].activated:
                                self.send('PRIVMSG {0} :[!] module {1} is already enabled'.format(sendto, buffparts[4]))
                            else:
                                self.send('PRIVMSG {0} :[+] enabling module: {1}'.format(sendto, buffparts[4]))
                                self.modules[module].activated = True
                return

        # ---------------------------------------------------------------------
        # if command is a module trigger, run it
        # ---------------------------------------------------------------------
        if cmd in self.modules:
            # check if module is activated
            if self.modules[cmd].activated:
                try:
                    # is it a command for admins only?
                    if self.modules[cmd].config['allow'] == 'admin':
                        if self.checkauth(buffparts[0]):
                            self.modules[cmd]._cmd_(sendto, buffparts)
                        else:
                            self.send('PRIVMSG {0} :[!] only authorized users can run this command'.format(sendto))
                    # else run guest module
                    else:
                        self.modules[cmd]._cmd_(sendto, buffparts)
                except Exception as error:
                    logging.error('module {0} error on line {1}: {2}'.format(cmd, sys.exc_info()[-1].tb_lineno, error))
                    
            else:
                self.send('PRIVMSG {0} :[!] module {1} is not activated'.format(sendto, self.modules[cmd].config['name']))
            return

        # ---------------------------------------------------------------------
        # no idea what the user asked for, echo it back for debugging
        # ---------------------------------------------------------------------
        #self.send('PRIVMSG {0} :{1}'.format(sendto, ' '.join(buffparts)))

    # ---------------------------------------------------------------------
    # message sent to bot with listener trigger
    # ---------------------------------------------------------------------
    def tolisteners(self, buffparts):
        # send to channel by default
        sendto = buffparts[2]
        # if buffparts[2] is the botname send to user
        if (buffparts[2] == self.nick):
            sendto = buffparts[0].split('!')[0][1:]

        for module in self.modules:
            mod = self.modules[module]
            if mod.config['trigger'] == '_listener_':
	        try:
                    mod._cmd_(sendto, buffparts)
	        except Exception as error:
	            logging.error('module {0} error on line {1}: {2}'.format(mod.config['name'], sys.exc_info()[-1].tb_lineno, error))

    # ---------------------------------------------------------------------
    # main thread loop parsing IRC messages
    # ---------------------------------------------------------------------
    def loop(self):
        logging.debug('loop started')
        # ---------------------------------
        while not self.exitFlag:
            try:
                self.rbuffer = self.irc.recv(self.sbuffer)
            except socket.timeout:
                logging.critical('socket timeout..')
                return
            except socket.error:
                logging.critical('lost connection..')
                return
            except:
                logging.critical('unexpected error..')
                return

            # parse IRC message
            reply = self.rbuffer.split('\n')
            for line in reply:
                if len(line.strip()) > 0:
                    # log line
                    logging.debug(line)
            
                # store server reply in a list (split by whitespace)
                buffparts = line.split()
                
                # :[user]![realname]@[ip] PRIVMSG [#channel] :[message]
                # ^---reply_token[0]----^ ^-[1]-^ ^--[2]---^  ^--[3]--^
                if len(buffparts) > 1:
                    # check if it's a command number
                    if buffparts[1].isdigit():
                        cmd = int(buffparts[1])
                        
                        # trigger appropriate command depending on value
                        # auto join on connect
                        if cmd == 1 or cmd == 376:
                            # if password auth with nickserv
                            if self.nickpass is not None:
                                self.send('PRIVMSG nickserv :IDENTIFY {0}'.format(self.nickpass))
                            # join channels
                            for chan in self.chans:
                                self.send('JOIN {0}'.format(chan))

                        # auto rename if already in use, ghost and ident to regain it if bot is registered
                        if cmd == 433:
                            self.send('NICK ctfbot_____')
                            # if password ghost nick auth
                            if self.nickpass is not None:
                                #self.send('PRIVMSG nickserv :GHOST {0} {1}'.format(self.nick, self.nickpass))
                                self.send('PRIVMSG nickserv :RECOVER {0} {1}'.format(self.nick, self.nickpass))
                                self.send('NICK {0}'.format(self.nick))
                                self.send('PRIVMSG nickserv :IDENTIFY {0}'.format(self.nickpass))

                    # reply to PING
                    if buffparts[0] == 'PING':
                        self.send('PONG {0}'.format(buffparts[1]))
                    
                    # if error quit thread loop
                    if buffparts[0] == 'ERROR':
                        logging.error('unexpected error: {0}'.format(line))
                        return
                        
                    # auto join after kick
                    if buffparts[1] == 'KICK':
                        self.send('JOIN {0}'.format(buffparts[2]))
                        self.send('PRIVMSG {0} :[?] Hey! Why would you do that?'.format(buffparts[2]))

                    # on privmsg parse cmd
                    if buffparts[1] == 'PRIVMSG':
                        buffparts[3] = buffparts[3][1:]
                        # make sure it's a trigger command (ex: !)
                        if buffparts[3][:len(self.trigger)] == self.trigger:
                            # remove trigger from command and parse request
                            buffparts[3] = buffparts[3][len(self.trigger):]
                            cmd = buffparts[3]
                            self.parsecmd(cmd, buffparts)
                        # else send content to modules with listener trigger
                        else:
                            self.tolisteners(buffparts)

        # ---------------------------------
        logging.debug('loop ended')
