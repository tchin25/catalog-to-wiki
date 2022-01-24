from pywikibot import family

# for local testing of updates to api.wikimedia.org

class Family(family.Family):
    name = 'api'
    # domain = 'api.wikimedia.org'
    langs = {
        'en': 'api.wikimedia.org/',
    }

    def protocol(self, code):
      return 'HTTPS'