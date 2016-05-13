from template import template

import logging

import duckduckgo, google
import requests, bs4

class search(template):
    def __init__(self, send):
        # class inheritance
        template.__init__(self, send)
        self.config = {
                        'name':        self.__class__.__name__,
                        'trigger':     'search',
                        'description': 'Search the web.',
                        'allow':       'guest',
                    }
        self.help = [
                        ['ARGUMENT', 'DESCRIPTION'],
                        ['query',  'Query to search for.'],
                    ]
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...
        
        if buffparts >= 5:

            query = ' '.join(buffparts[4:])

            # search duckduckgo
            response = duckduckgo.query(query)

            # if there's an instant answer
            if response.type != "nothing":

                # format response string (could be sexier)
                rstring = response.heading + ' -> '
                if response.abstract.text != "":
                    rstring += response.abstract.text
                if response.abstract.url != "":
                    rstring += ' [' + response.abstract.url + '] '

            # if there's no adequate answer
            elif response.type == "nothing" or response.type== "":
                notice =  'No instant answers from DuckDuckGo. '
                notice += 'Retrieving the first Google result..'
                self.send('PRIVMSG {0} :{1}'.format(sendto, notice))

                #search google instead
                for url in google.search(query, num=1, stop=1):
                    
                    # get title
                    r = requests.get(url)
                    html = bs4.BeautifulSoup(r.text, "html.parser")
                    rstring = html.title.text

                    # add url
                    rstring += ' [' + url + '] '


            self.send('PRIVMSG {0} :{1}'.format(sendto, rstring))

        return
