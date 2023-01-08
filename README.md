# Code Archive for "What The Place?" (whattheplace.com)

Code archive for whattheplace.com, a Python-/Django-based web game about guessing the location where a picture has been taken.

This project was actively developed between 2009 and ~2012 and the webpage operated/maintained until 2018.

Since the page is no longer live, have a look at the Internet Archive (e.g., https://web.archive.org/web/20110208013656/http://www.whattheplace.com/) or the screenshots below to see what it looked like.

[![Screenshot: Home](/screenshot_home_scaled.png)](/screenshot_home.png)
[![Screenshot: Hall Of Fame](/screenshot_hall_of_fame_scaled.png)](/screenshot_hall_of_fame.png)
[![Screenshot: Stats](/screenshot_stats_scaled.png)](/screenshot_stats.png)
[![Screenshot: Login](/screenshot_login_scaled.png)](/screenshot_login.png)

## Necessary Packages (from old README)

**Note (2022): The requirements.txt file is provided as it was on the time. Getting the code to work today problably will not work with the packages from the PyPI and would require to obtain the legacy package versions from somewhere else.**

See requirements.txt

To compile PIL:
```
sudo apt-get install python-dev
```

Enabling JPEG support in PIL (tested on Ubuntu 13.04 and 13.10):
```
sudo apt-get install libjpeg62 libjpeg62-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
```

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
