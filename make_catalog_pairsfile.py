#!/usr/bin/python

# This script retrieves API Catalog info from backstage as a json
# string, converts the json to wikitext, and stores the wikitext
# to a local file suitable for use by the replace.py script.
#
# Most functions herein don't do much error handling.
# Instead, exceptions will be thrown, which is messy but effective.
# If we ever want to be prettier, download_dump.py has some relevant 
# code that we could use as inspiration.

import json
import pywikibot
from pywikibot.comms import http
# from pywikibot import pagegenerators, textlib

BACKSTAGE_URL = 'https://backstage-api-catalog.toolforge.org/api/catalog/entities?filter=kind=api'
OUTPUT_FILE = './pairsfile.txt'
PAIRSFILE_REGEX = '<!-- BEGIN API LIST -->.*<!-- END API LIST -->'

# ===========================================================
# retrieves the catalog json as a string from backstage
# ===========================================================
def fetchCatalogJson():
	url = BACKSTAGE_URL
	response = http.fetch(url)
	if not response.content:
		pywikibot.output('No catalog json content available. Quitting.')
		quit()
	return response.content    

# ===========================================================
# parses the catalog json string into an object
# ===========================================================
def parseCatalogJson(catalogJson):
	return json.loads(catalogJson)

# ===========================================================
# makes a single field entry string for use in api wikitext
# ===========================================================
def makeFieldWikitext(name, value):
	return name + ': ' + value + '<br>'

# ===========================================================
# converts a single api object to wikitext
# ===========================================================
def convertApiToWikitext(apiInfo):
	wikitext = '<li>'
	wikitext += makeFieldWikitext('Name', apiInfo['metadata']['name'])
	wikitext += makeFieldWikitext('Description', apiInfo['metadata']['description'])
	wikitext += makeFieldWikitext('Link', apiInfo['metadata']['annotations']['backstage.io/view-url'])
	for relation in apiInfo['relations']:
		if relation['type'] == 'ownedBy':
			wikitext += makeFieldWikitext('Owner:', relation['target']['name'])
	wikitext += '</li><br>'		
	return wikitext

# ===========================================================
# converts the catalog object to wikitext
# ===========================================================
def convertCatalogToWikitext(catalogInfo):
	wikitext = '<ul>'
	for api in catalogInfo:
		wikitext += convertApiToWikitext(api)
	wikitext += '</ul>'	
	return wikitext	

# ===========================================================
# prepares the pairsfile contents
# ===========================================================
def makePairsfileContents(wikitext):
	contents = PAIRSFILE_REGEX + '\n'
	contents += '<!-- BEGIN API LIST -->'
	contents += wikitext
	contents += '<!-- END API LIST -->'
	return contents

# ===========================================================
# writes a pairsfile suitable for the replace.py script
# ===========================================================
def savePairsfile(wikitext):
	with open(OUTPUT_FILE, 'w') as result_file:
		result_file.write(wikitext)

# ===========================================================
# main script routine
# ===========================================================
def main():
	pywikibot.output('------- begin bdp_test_one.py -------');

	catalogJson = fetchCatalogJson()
	catalogInfo = parseCatalogJson(catalogJson)
	catalogWikitext = convertCatalogToWikitext(catalogInfo)
	contents = makePairsfileContents(catalogWikitext)
	savePairsfile(contents);

	pywikibot.output('------- end bdp_test_one.py -------');

# ===========================================================
#  script entry point
# ===========================================================
main()    