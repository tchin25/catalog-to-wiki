#!/bin/sh

# note: make sure core/user-config.py is set up for the appropriate wiki

printf "Begin Bash Script\n"

python3 ../../pwb.py make_catalog_pairsfile.py

# this is for testing against api.wikimedia.org
python3 ../../pwb.py ./replace.py -page:API_catalog -regex -dotall -always -automaticsummary -pairsfile:pairsfile.txt

# this is for testing against my local wiki
# python3 ../../pwb.py ./replace.py -page:pywikibot_test -regex -dotall -always -automaticsummary -pairsfile:pairsfile.txt

# this put the search/replace string directly in the command rather than using a pairsfile
# python3 ../../pwb.py ./replace.py -page:pywikibot_test -regex -dotall -always -automaticsummary "<!-- BEGIN API LIST -->.*<!-- END API LIST -->" "<!-- BEGIN API LIST -->foo<!-- END API LIST -->"

printf "End Bash Script\n"
