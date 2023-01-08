from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import tweepy

from wtp import auth, models

class TwitterAuthBackend:
  def authenticate(self, twitterAccessKey, twitterAccessSecret):
    userProfiles = models.UserProfile.objects.filter(twitterAccessKey = twitterAccessKey,
                                                     twitterAccessSecret = twitterAccessSecret)
    if userProfiles:
      return userProfiles[0].user
    else:
      return None
  
  def get_user(self, id):
    try:
      return User.objects.get(pk = id)
    except:
      return None

def checkTwitterAccess(twitterAccessKey, twitterAccessSecret):
  try:
    twitterAuth = getTwitterAuth()
    twitterAuth.set_access_token(twitterAccessKey, twitterAccessSecret)
    
    api = tweepy.API(twitterAuth)
    api.me()
    
    return True
  except tweepy.TweepError:
    return False

def disableTwitter(user):
  userProfile = user.get_profile()
  
  userProfile.twitterAccessKey = None
  userProfile.twitterAccessSecret = None
  userProfile.twitterAutoTweet = False
  userProfile.save()
  
  user.tweet_set.update(active = False)

def enableTwitter(user, accessToken):
  try:
    userProfile = user.get_profile()
    userProfile.twitterAccessKey = accessToken.key
    userProfile.twitterAccessSecret = accessToken.secret
    userProfile.save()
    
    return True
  except tweepy.TweepError:
    return False

def exchangeVerifierForAccessToken(requestToken, oAuthVerifier):
  try:
    twitterAuth = getTwitterAuth()
    twitterAuth.set_request_token(requestToken[0], requestToken[1])
    twitterAuth.get_access_token(oAuthVerifier)
    
    return twitterAuth.access_token
  except tweepy.TweepError:
    return None

def getNickname(accessToken):
  try:
    twitterAuth = getTwitterAuth()
    twitterAuth.set_access_token(accessToken.key, accessToken.secret)
    
    return twitterAuth.get_username()
  except tweepy.TweepError:
    return ""

def getTwitterAuth():
  return tweepy.OAuthHandler(settings.TWITTER_CONSUMERKEY, settings.TWITTER_CONSUMERSECRET, settings.BASE_URL + 
                             reverse("wtp.views.twitterCallback"))

def hasTwitter(user):
  userProfile = user.get_profile()
  return userProfile.twitterAccessKey and userProfile.twitterAccessSecret

def isUserRegistered(accessToken):
  userProfiles = models.UserProfile.objects.filter(twitterAccessKey = accessToken.key,
                                                   twitterAccessSecret = accessToken.secret)
  return userProfiles.exists()

def registerTwitterUser(form):
  user = User.objects.create(username = form.cleaned_data["nickname"], email = form.cleaned_data["mailaddress"])
  user.set_unusable_password()
  user.save()
  
  models.UserProfile.objects.create(user = user, twitterAccessKey = form.cleaned_data["twitterAccessKey"],
                                    twitterAccessSecret = form.cleaned_data["twitterAccessSecret"])
  
  if user.email:
    auth.sendConfirmKey(user)

def sendActiveTweets():
  skipUsers = []
  activeTweets = models.Tweet.objects.filter(active = True)
  
  for tweet in activeTweets:
    user = tweet.user
    
    if not tweet.user in skipUsers:
      userProfile = user.get_profile()
      
      if sendTweet(tweet):
        userProfile.twitterFailedAttempts = 0
        userProfile.save()
      else:
        skipUsers.append(user)
        
        userProfile.twitterFailedAttempts += 1
        userProfile.save()
        
        if userProfile.twitterFailedAttempts > 20:
          disableTwitter(user)

def sendTweet(tweet):
  userProfile = tweet.user.get_profile()
  
  if not userProfile.twitterAccessKey or not userProfile.twitterAccessSecret:
    return False
  
  try:
    twitterAuth = getTwitterAuth()
    twitterAuth.set_access_token(userProfile.twitterAccessKey, userProfile.twitterAccessSecret)
    
    api = tweepy.API(twitterAuth)
    api.update_status(tweet.text)
    
    tweet.timestampSent = datetime.now()
    tweet.active = False
    tweet.save()
     
    return True
  except tweepy.TweepError:
    return False

def startTwitterAuth():
  try:
    twitterAuth = getTwitterAuth()
    authUrl = twitterAuth.get_authorization_url()
    
    return {"url": authUrl, "requestToken": (twitterAuth.request_token.key, twitterAuth.request_token.secret)}
  except tweepy.TweepError:
    return None

def tweetImageSolved(user, image):
  userProfile = user.get_profile()
  
  if not userProfile.twitterAccessKey or not userProfile.twitterAccessSecret or not userProfile.twitterAutoTweet:
    return True
  
  msg = (userProfile.twitterMessage if userProfile.twitterMessage else
         "Just solved image #%ID% on What The Place! %URL% #wtp")
  msg = msg.replace("%ID%", str(image.id))
  msg = msg.replace("%URL%", settings.BASE_URL + reverse("wtp.views.showImage", kwargs = {"imageId": image.id}))
  
  tweet = models.Tweet.objects.create(user = user, text = msg)
  
  sendTweet(tweet)
