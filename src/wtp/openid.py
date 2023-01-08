from __future__ import absolute_import
import base64
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from hashlib import md5
from openid.association import Association
from openid.consumer.consumer import Consumer, SUCCESS
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import ax, sreg
from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW
import time

from wtp import auth, models

# From django_openid: http://github.com/simonw/django-openid/blob/master/django_openid/models.py
class DjangoOpenIDStore(OpenIDStore):
  def storeAssociation(self, server_url, association):
    assoc = models.OpenIDAssociation(server_url = server_url, handle = association.handle,
                                     secret = base64.encodestring(association.secret), issued = association.issued,
                                     lifetime = association.issued, assoc_type = association.assoc_type)
    assoc.save()
  
  def getAssociation(self, server_url, handle = None):
    assocs = []
    if handle is not None:
      assocs = models.OpenIDAssociation.objects.filter(server_url = server_url, handle = handle)
    else:
      assocs = models.OpenIDAssociation.objects.filter(server_url = server_url)
    if not assocs:
        return None
    associations = []
    for assoc in assocs:
      association = Association(assoc.handle, base64.decodestring(assoc.secret), assoc.issued, assoc.lifetime,
                                assoc.assoc_type)
      if association.getExpiresIn() == 0:
        self.removeAssociation(server_url, assoc.handle)
      else:
        associations.append((association.issued, association))
    if not associations:
      return None
    return associations[-1][1]
  
  def removeAssociation(self, server_url, handle):
    assocs = list(models.OpenIDAssociation.objects.filter(server_url = server_url, handle = handle))
    assocs_exist = len(assocs) > 0
    for assoc in assocs:
      assoc.delete()
    return assocs_exist
  
  def useNonce(self, server_url, timestamp, salt):
    # Has nonce expired?
    if abs(timestamp - time.time()) > SKEW:
      return False
    try:
      nonce = models.OpenIDNonce.objects.get(server_url__exact = server_url, timestamp__exact = timestamp,
                                             salt__exact = salt)
    except models.OpenIDNonce.DoesNotExist:
      nonce = models.OpenIDNonce.objects.create(server_url = server_url, timestamp = timestamp, salt = salt)
      return True
    nonce.delete()
    return False
  
  def cleanupNonce(self):
    models.OpenIDNonce.objects.filter(timestamp__lt = (int(time.time()) - SKEW)).delete()
  
  def cleanupAssociations(self):
    models.OpenIDAssociation.objects.extra(where = ["issued + lifetimeint < (%s)" % time.time()]).delete()
  
  def getAuthKey(self):
    # Use first AUTH_KEY_LEN characters of md5 hash of SECRET_KEY
    return md5.new(settings.SECRET_KEY).hexdigest()[:self.AUTH_KEY_LEN]
  
  def isDumb(self):
    return False

class OpenIDAuthBackend:
  def authenticate(self, openIDUrl):
    openIDConnections = models.UserOpenID.objects.filter(url = openIDUrl)
    if openIDConnections:
      return openIDConnections[0].user
    else:
      return None
  
  def get_user(self, id):
    try:
      return User.objects.get(pk = id)
    except:
      return None

def disableOpenID(user, url):
  user.useropenid_set.filter(url = url).delete()

def enableOpenID(user, url):
  if not models.UserOpenID.objects.filter(user = user, url = url).exists():
    user.useropenid_set.create(user = user, url = url)

def finishOpenIDAuth(request, parameters):
  consumer = getOpenIDConsumer(request)
  
  redirectTarget = settings.BASE_URL + reverse("wtp.views.openIDCallback")
  response = consumer.complete(parameters, redirectTarget)
  
  if response.status != SUCCESS:
    return None
  
  mailAddress = None
  
  axResponse = ax.FetchResponse.fromSuccessResponse(response)
  if axResponse:
    mailAddress = axResponse.get("http://schema.openid.net/contact/email")[0]
  else:
    sregResponse = sreg.SRegResponse.fromSuccessResponse(response)
    if sregResponse and "email" in sregResponse:
      mailAddress = sregResponse["email"]
  
  if not mailAddress:
    return None
  
  return {"url": response.getDisplayIdentifier(), "mailAddress": mailAddress}

def getAuthStartUrl(request, identity):
  consumer = getOpenIDConsumer(request)
  
  try:
    authRequest = consumer.begin(identity)
  except DiscoveryFailure:
    return None
  
  sregRequest = sreg.SRegRequest(optional = ["email"])
  authRequest.addExtension(sregRequest)
  
  axRequest = ax.FetchRequest()
  axRequest.add(ax.AttrInfo("http://schema.openid.net/contact/email", required = True))
  authRequest.addExtension(axRequest)
  
  trustRoot = settings.BASE_URL
  redirectTarget = settings.BASE_URL + reverse("wtp.views.openIDCallback")
  
  redirectUrl = authRequest.redirectURL(trustRoot, redirectTarget)
  
  return redirectUrl

def getOpenIDConsumer(request):
  return Consumer(request.session, DjangoOpenIDStore())

def getOpenIDIdentities(user):
  return user.useropenid_set.values("url")

def isUserRegistered(url):
  userProfiles = models.UserOpenID.objects.filter(url = url)
  return userProfiles.exists()

def registerOpenIDUser(form):
  user = User.objects.create(username = form.cleaned_data["nickname"], email = form.cleaned_data["mailaddress"])
  user.set_unusable_password()
  user.save()
  
  models.UserProfile.objects.create(user = user)
  user.useropenid_set.create(user = user, url = form.cleaned_data["url"])
  
  if user.email:
    auth.sendConfirmKey(user)
