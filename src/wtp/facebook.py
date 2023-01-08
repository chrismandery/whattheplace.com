from __future__ import absolute_import
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from facebook import GraphAPI
import urllib
from cgi import parse_qs

from wtp import auth, models

class FacebookAuthBackend:
  def authenticate(self, facebookId):
    userProfiles = models.UserProfile.objects.filter(facebookId = facebookId)
    if userProfiles:
      return userProfiles[0].user
    else:
      return None
  
  def get_user(self, id):
    try:
      return User.objects.get(pk = id)
    except:
      return None

def disableFacebook(user):
  userProfile = user.get_profile()
  
  userProfile.facebookId = None
  userProfile.save()

def enableFacebook(user, facebookId):
  userProfile = user.get_profile()
  
  userProfile.facebookId = facebookId
  userProfile.save()

def exchangeCodeForAccessToken(code):
  args = {"client_id": settings.FACEBOOK_APPID,
          "redirect_uri": settings.BASE_URL + reverse("wtp.views.facebookCallback"),
          "type": "web_server",
          "client_secret": settings.FACEBOOK_APPSECRET,
          "code": code}
  try:
    response = parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + 
                                       urllib.urlencode(args)).read())
    accessToken = response["access_token"][-1]
  except:
    return None
  
  return accessToken

def getAuthStartUrl():
  args = {"client_id": settings.FACEBOOK_APPID,
          "redirect_uri": settings.BASE_URL + reverse("wtp.views.facebookCallback"),
          "type": "web_server"}
  
  return "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)

def getFacebookId(accessToken):
  try:
    graph = GraphAPI(accessToken)
    me = graph.get_object("me")
    
    return me["id"]
  except:
    return None

def getNickname(accessToken):
  try:
    graph = GraphAPI(accessToken) 
    me = graph.get_object("me")
    
    return me["first_name"] + me["last_name"][0]
  except:
    return None

def hasFacebook(user):
  userProfile = user.get_profile()
  return bool(userProfile.facebookId)

def isUserRegistered(accessToken, facebookId):
  userProfiles = models.UserProfile.objects.filter(facebookId = facebookId)
  return userProfiles.exists()

def registerFacebookUser(form):
  user = User.objects.create(username = form.cleaned_data["nickname"], email = form.cleaned_data["mailaddress"])
  user.set_unusable_password()
  user.save()
  
  models.UserProfile.objects.create(user = user, facebookId = form.cleaned_data["facebookId"])
  
  if user.email:
    auth.sendConfirmKey(user)
