#!/bin/sh

printf "Begin Bash Script\n"

python3 ../../pwb.py make_catalog_pairsfile.py

python3 ../../pwb.py ./replace.py -page:pywikibot_test -regex -dotall -always -automaticsummary -pairsfile:pairsfile.txt

# python3 ../../pwb.py ./replace.py -page:pywikibot_test -regex -dotall -always -automaticsummary "<!-- BEGIN API LIST -->.*<!-- END API LIST -->" "<!-- BEGIN API LIST -->foo<!-- END API LIST -->"

# python3 ../../pwb.py ./replace.py -page:pywikibot_test -regex -dotall -always -automaticsummary foobar foobaz

printf "End Bash Script\n"
