import os
import site
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wtp.settings")

vepath = '/home/whattheplace/whattheplace/lib/python2.7/site-packages'
prev_sys_path = list(sys.path)
site.addsitedir(vepath)
sys.path.append('/home/whattheplace/whattheplace/src')
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
