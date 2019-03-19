#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Mike Shultz'
SITENAME = 'Mike Shultz'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Denver'

DEFAULT_LANG = 'en'

THEME = 'themes/mike'

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['assets',]#'yuicompressor', ]

ASSET_SOURCE_PATHS = ['static/css']
ASSET_CONFIG = (
    ('closure_compressor_optimization', 'WHITESPACE_ONLY'),
    ('less_bin', 'lessc'),
)

#STATIC_PATHS = ['static']
THEME_STATIC_DIR = 'static'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
