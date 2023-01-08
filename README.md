# Code archive for "What The Place?" (whattheplace.com)

Code archive for whattheplace.com, a Python-/Django-based web game about guessing the location where a picture has been taken.

This project was actively developed between 2009 and ~2012 and the webpage operated/maintained until 2018.

## Necessary Packages (from old README)

See requirements.txt

To compile PIL:
sudo apt-get install python-dev

Enabling JPEG support in PIL (tested on Ubuntu 13.04 and 13.10):
sudo apt-get install libjpeg62 libjpeg62-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so

- >= Django 1.2
- python-openid
- http://github.com/facebook/python-sdk/
- Tweepy

## Coding Conventions (from old README)

Python:
- Indentation: 2 space
- Line length: 120 characters
- Use " for string literals

Templates:
- Indentation: 1 tab
- Tab width: 4
- Line length: 120 characters
- Content in template tags like {% if %} is also indented
- Indentation after line breaks in HTML tags
- Top level blocks (e.g. {% block content %}) are not indented
