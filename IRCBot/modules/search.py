from template import template

import logging
import duckduckgo, requests, re, json
# ---------------------------------------------------------------
# WARNING: BINGAPIKEY must be declared in IRCBot/settings.py
# ---------------------------------------------------------------
from IRCBot import settings

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
        self.charlimit = 200
        
    def _cmd_(self, sendto, buffparts):
        #:[user]![name]@[IP] [PRIVMSG] [#chan] [cmd] [arg1] [arg2] [...]
        #   ^-----0-----^        1        2      3      4      5    ...

        if len(buffparts) == 5  and re.match(r'CVE-\d{4}-\d{4,}', buffparts[4]):
            try:
	        cve_url = 'http://cve.circl.lu/api/cve/{0}'.format(buffparts[4])
	        results = json.loads(requests.get(cve_url).text)
                # make sure we have a summary in the JSON object
                if results.has_key('summary') is False:
                    rstring = "The search retrieved no results."
                    self.send('PRIVMSG {0} :{1}'.format(sendto, rstring))
                    return
		summary = results['summary']
	        if len(summary) > self.charlimit:
		    summary = summary[:self.charlimit] + '..'
                cvss = results['cvss']
                sciplink = results['map_cve_scip']['sciplink']
	        rstring = "[CVE] {0} [CVSS: {1}] -> {2} [{3}]".format(buffparts[4], cvss, summary, sciplink)
                self.send('PRIVMSG {0} :{1}'.format(sendto, rstring))
            except Exception as e:
                logging.error('search CVE error: {0}'.format(e))
        
        elif len(buffparts) >= 5:

            query = ' '.join(buffparts[4:])

            # search duckduckgo
            response = duckduckgo.query(query)

            # trivial answer
            if response.type == "answer":

                name = response.heading

                # get description, and cut it short
                description = response.abstract.text
                if len(description) > self.charlimit:
                    description = description[:self.charlimit] + '..'

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
                
                # replace useful html tags (more to be found)
                answer = re.sub('<sup>', '^', answer)

                # strip useless html tags that come with the answer
                answer = re.sub('<.*?>', '', answer)

                rstring = "[DuckDuckGo] {0}".format(answer)

            # if DuckDuckGo doesn't have an instant answer, go to bing
            elif getattr(settings, 'BINGAPIKEY', None) is not None and (response.type == "nothing" or response.type == ""):

                # query the api
                query = '%20'.join(buffparts[4:])
                bing_url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/Web?Query=%27{0}%27&Market=%27en-US%27&$format=json'.format(query)
                results = json.loads(requests.get(bing_url, auth=(settings.BINGAPIKEY, settings.BINGAPIKEY)).text)

                # if there is results
                if len(results['d']['results']) > 0:

                    title = results['d']['results'][0]['Title'].encode('utf-8').strip()

                    description = results['d']['results'][0]['Description'].encode('utf-8').strip()

                    if len(description) > self.charlimit:
                        description = description[:self.charlimit] + '..'

                    url = results['d']['results'][0]['Url']

                    rstring = "[Bing] {0} -> {1} [{2}]".format(title, description, url)

                else:
                    rstring = "The search retrieved no results."

            self.send('PRIVMSG {0} :{1}'.format(sendto, rstring))

        return
