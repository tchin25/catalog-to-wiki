from pywikibot import family

# for local mw-cli dev wiki

class Family(family.Family):
    name = 'mwcli'
    langs = {
        'en': 'default.mediawiki.mwdd.localhost:8080/',
    }
