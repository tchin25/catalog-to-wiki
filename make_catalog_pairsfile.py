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
from string import Template
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
# creates a styled card
# ===========================================================
def createCard(title, tag, description, link):
	return Template(
	'''
 	<div class="col-sm">
	<div class="card" style="background: #f8f9fa; border: 1px solid #eaecf0; min-height:180px; height: 100%">
	<div class="card-body">
	<p class="card-title" style="font-weight:600;">$title</p>
	{{Tag|$tag}}
	<p class="card-text" style="font-size: 14px;
	overflow: hidden;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
 	">$description</p>
	<p class="card-text" style="font-size: 14px;">[$link Read the docs]</p>
	</div>
	</div>
	</div>
	'''
	).substitute({
		'title': title,
		'tag': tag,
		'description': description,
		'link': link
	})
 
# ===========================================================
# creates a formatted row
# ===========================================================
def createRow(apiCards):
	wikitext = '<div class="row" style="padding-top:20px;">'
	for apiCard in apiCards:
		wikitext += createCard(**apiCard)
	wikitext += '</div>'
	return wikitext

# ===========================================================
# wraps wikitext in a div container
# ===========================================================
def createContainer(wikitext):
    return '<div class="container">{0}</div>'.format(wikitext)
 
# ===========================================================
# extracts wanted properties of each api from catalog JSON
# and puts it in a dict array
# ===========================================================
def extractApiInfo(catalogObject):
	apiCards = []
	for apiInfo in catalogObject:
		apiCards += [{
			'title': transformTitle( apiInfo.get('metadata', {}).get('name', '') ),
			'description': apiInfo.get('metadata', {}).get('description', ''),
			'tag': apiInfo.get('spec', {}).get('lifecycle', ''),
			'link': apiInfo.get('metadata', {}).get('links', [{}])[0].get('url', '')
		}]
	return apiCards

def transformTitle(title):
    return title.replace('-', ' ').title()

# ===========================================================
# prepares the pairsfile contents
# formatted into rows of 3 cards
# ===========================================================
def generateApiWikitext(catalogObject):
    apiCards = extractApiInfo(catalogObject)
    wikitext = ''
    for apiRow in chunks(apiCards, 3):
        wikitext += createRow(apiRow)
    wikitext = createContainer(wikitext)
    return wikitext
    
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# ===========================================================
# prepares the pairsfile contents
# ===========================================================
def makePairsfileContents(wikitext):
	# First line is the search string
	# Second line is the replacement string
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
		result_file.close();

# ===========================================================
# main script routine
# ===========================================================
def main():
	pywikibot.output('------- begin make_catalog_pairsfile.py -------');

	catalogJson = fetchCatalogJson()
	catalogInfo = parseCatalogJson(catalogJson)
	# catalogWikitext = convertCatalogToWikitext(catalogInfo)
	catalogWikitext = generateApiWikitext(catalogInfo)
	contents = makePairsfileContents(catalogWikitext.replace('\n',' '))
	savePairsfile(contents);

	pywikibot.output('------- end make_catalog_pairsfile.py -------');

# ===========================================================
#  script entry point
# ===========================================================
main()    
