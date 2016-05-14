from template import template

import logging
import duckduckgo, requests, re, json

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

            # trivial answer
            if response.type == "answer":

                name = response.heading

                # get description, and cut it short
                description = response.abstract.text
                if len(description) > 300:
                    description = description[:300]

                url = response.abstract.url
                
                rstring = "[DuckDuckGo] {0} -> {1} [{2}]".format(name, description, url)

            # some things mean many things
            elif response.type == "disambiguation":

                name = response.heading

                url = response.abstract.url

                rstring = "[DuckDuckGo] {0} can be several things. [{1}]".format(name, url)

            # some things include other things
            elif response.type == "category":

                name = response.heading

                url = response.abstract.url

                rstring = "[DuckDuckGo] {0} is a category. [{1}]".format(name, url)

            # other types of answer (calculations, etc)
            elif response.type == "exclusive":

                answer = response.answer.text
                # strip useless html tags that come with the answer
                answer = re.sub('<.*?>', '', answer)

                rstring = "[DuckDuckGo] {0}".format(answer)

            # if DuckDuckGo doesn't have an instant answer, go to bing
            elif response.type == "nothing" or response.type == "":

                # query the api
                bing_key = "API_KEY"
                query = '%20'.join(buffparts[4:])
                bing_url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%27{0}%27&$format=json'.format(query)
                results = json.loads(requests.get(bing_url, auth=(bing_key, bing_key)).text)

                # if there is results
                if len(results['d']['results']) > 0:

                    title = results['d']['results'][0]['Title'].encode('utf-8').strip()

                    description = results['d']['results'][0]['Description'].encode('utf-8').strip()
                    if len(description) > 200:
                        description = description[:200]

                    url = results['d']['results'][0]['Url']

                    rstring = "[Bing] {0} -> {1} [{2}]".format(title, description, url)

                else:
                    rstring = "The search retrieved no results."

            self.send('PRIVMSG {0} :{1}'.format(sendto, rstring))

        return
