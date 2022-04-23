# catalog-to-wiki

This repo has been manually moved to the [Wikimedia Foundation's Gitlab instance](https://gitlab.wikimedia.org/repos/api-platform/catalog-to-wiki). Future updates will be made there.

Scripts for updating an on-wiki API catalog based on Backstage data

Context:
WMF is evaluating an API catalog based on Backstage (and open source platform
originally created by Spotify, later given to the CNCF). WMF also has an existing
API Portal wiki for API-related documentation. The scripts herein are for
mirroring certain data from Backstage into the API Portal.

Approach:
Several implementations would have been possible, including use a Special Page
via a Mediawiki extension. However, at least for an experimental project, it
was faster and more convenient to do this via a bot. Specifically, a Pywikibot
script was created to fetch JSON information from Backstage, convert it into
wikitext, and push it to the wiki.

Notes:
There's no reason a Pywikibot script was necessary for pulling/converting the
information, but it was straightforward and kept the implementation consistent.
Rather than add the text replacement code into the new script, the existing
Pywikibot replace.py was used. A Bash script coordinates the two Pywikibot scripts.

This respository is just a place to stuff files so they don't exist only on my
laptop. It isn't a ready-to-pull-and-run project.

I performed local testing on a local wiki created via mwcli:
  https://www.mediawiki.org/wiki/Cli
I therefore had a core/pywikibot/families/mwcli_family.py file, which I referenced
in core/user-config.py.  

This is an experimental proof-of-concept and is unsuited for production use.
