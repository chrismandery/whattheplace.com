from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django import http, template
from re import compile

from wtp import helper, models

class TrackingMiddleware:
  def process_response(self, request, response):
    # This happens only if CommonMiddleware issues a redirect before SessionMiddleware is run
    if not hasattr(request, "session"):
      return response
    
    if not "sessionKey" in request.session:
      request.session["sessionKey"] = helper.generateAlNumString(40)
    
    models.PageHit.objects.create(sessionKey = request.session["sessionKey"], path = request.path,
                           statusCode = response.status_code)
    
    return response
