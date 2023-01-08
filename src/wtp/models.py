from django.contrib.auth.models import User
from django.db import models
from django.utils.html import escape

class UserProfile(models.Model):
  user = models.ForeignKey(User, unique = True, editable = False)
  confirmKey = models.CharField(max_length = 40, null = True, blank = True, unique = True)
  showInHallOfFame = models.BooleanField(default = True)
  showAsFirstSolver = models.BooleanField(default = True)
  showAsSolver = models.BooleanField(default = True)
  showPublicProfile = models.BooleanField(default = False)
  facebookId = models.BigIntegerField(null = True, blank = True, unique = True)
  twitterAccessKey = models.CharField(max_length = 255, null = True, blank = True, unique = True)
  twitterAccessSecret = models.CharField(max_length = 255, null = True, blank = True, unique = True)
  twitterMessage = models.CharField(max_length = 140, blank = True, default = "")
  twitterAutoTweet = models.BooleanField(default = False)
  twitterFailedAttempts = models.SmallIntegerField(default = 0)
  
  def __unicode__(self):
    return "User profile for " + self.user.username

class UserOpenID(models.Model):
  user = models.ForeignKey(User, editable = False)
  url = models.URLField(max_length = 200, unique = True, editable = False)
  
  def __unicode__(self):
    return "Authentification for " + self.user.username + " via " + self.url

# From django_openid: http://github.com/simonw/django-openid/blob/master/django_openid/models.py
class OpenIDAssociation(models.Model):
  server_url = models.TextField(max_length = 2047)
  handle = models.CharField(max_length = 255)
  secret = models.TextField(max_length = 255)
  issued = models.IntegerField()
  lifetime = models.IntegerField()
  assoc_type = models.TextField(max_length = 64)
  
  def __unicode__(self):
    return u"OpenID Association: %s, %s" % (self.server_url, self.handle)

# From django_openid: http://github.com/simonw/django-openid/blob/master/django_openid/models.py
class OpenIDNonce(models.Model):
  server_url = models.CharField(max_length = 255)
  timestamp = models.IntegerField()
  salt = models.CharField(max_length = 40)
  
  def __unicode__(self):
    return u"OpenID Nonce: %s for %s" % (self.salt, self.server_url)

class PageHit(models.Model):
  sessionKey = models.CharField(max_length = 40, editable = False)
  timestamp = models.DateTimeField(auto_now_add = True, editable = False)
  path = models.CharField(max_length = 255, editable = False)
  statusCode = models.SmallIntegerField(editable = False)
  
  def __unicode__(self):
    return (self.timestamp.strftime("%d.%m.%Y %H:%M:%S") + ": " + self.path + " " + str(self.statusCode) + " (" + 
            self.sessionKey[0:6] + "...)")

class TrafficDigest(models.Model):
  date = models.DateField(editable = False)
  hour = models.SmallIntegerField(null = True, editable = True)
  requests = models.IntegerField(editable = False)
  sessions = models.IntegerField(editable = False)
  users = models.IntegerField(editable = False)
  resolutions = models.IntegerField(editable = False)
  comments = models.IntegerField(editable = False)
  
  class Meta:
    unique_together = ("date", "hour")
  
  def __unicode__(self):
    return (self.date.strftime("%d.%m.%Y") + (" (total)" if self.hour == None else " (hour " + str(self.hour) + ")") + 
            ": " + str(self.requests) + " requests, " + str(self.sessions) + " sessions, " + str(self.users) + 
            " users, " + str(self.resolutions) + " resolutions, " + str(self.comments) + " comments")  

class SentMail(models.Model):
  recipient = models.CharField(max_length = 80, editable = False)
  timestamp = models.DateTimeField(auto_now_add = True, editable = False)
  subject = models.CharField(max_length = 80, editable = False)
  text = models.TextField(editable = False)
  
  def __unicode__(self):
    return self.timestamp.strftime("%d.%m.%Y %H:%M:%S") + ": " + self.recipient + " / " + self.subject

class Tweet(models.Model):
  user = models.ForeignKey(User, editable = False)
  timestampCreated = models.DateTimeField(auto_now_add = True, editable = False)
  timestampSent = models.DateTimeField(null = True, editable = False)
  active = models.BooleanField(default = True, editable = False)
  text = models.CharField(max_length = 140, editable = False)

class License(models.Model):
  name = models.CharField(max_length = 80, unique = True)
  visible = models.BooleanField(default = False)
  url = models.URLField(max_length = 200)
  description = models.TextField()
  
  def __unicode__(self):
    return self.name

class Image(models.Model):
  imageHash = models.CharField(max_length = 32, unique = True, editable = False)
  visible = models.BooleanField(default = False)
  uploader = models.ForeignKey(User, editable = False)
  hint = models.CharField(max_length = 100, blank = True)
  license = models.ForeignKey(License)
  author = models.CharField(max_length = 80, blank = True)
  source = models.URLField(max_length = 200, blank = True)
  dateAdded = models.DateTimeField(auto_now_add = True, editable = False)
  views = models.IntegerField(editable = False)
  
  def __unicode__(self):
    return "#" + str(self.id) + " by " + escape(self.uploader.username)
  
  def copyright(self):
    text = "License: " + escape(self.license.name)
    
    if self.author:
      text += "<br />Author: " + escape(self.author)
    
    if self.source:
      text += "<br />Source: <a href=\"" + escape(self.source) + "\">" + escape(self.source) + "</a>"
    
    return text
  
  copyright.allow_tags = True
  
  def thumbImage(self):
    return "<img src=\"/media/thumbs/" + escape(self.imageHash) + ".jpeg\" alt=\"Thumbnail\" />"
  
  thumbImage.allow_tags = True
  
  def solutions(self):
    solutions = [obj.value for obj in self.solution_set.filter(active = True)]
    text = ", ".join(solutions)
    
    solutions = [obj.value for obj in self.solution_set.filter(active = False)]
    if len(solutions):
      text += " | inactive: " + ", ".join(solutions)
    
    return text

class Solution(models.Model):
  image = models.ForeignKey(Image, editable = False)
  value = models.CharField(max_length = 40)
  active = models.BooleanField(default = False)
  
  class Meta:
    unique_together = ("image", "value")
  
  def __unicode__(self):
    if self.active:
      return "Active solution \"" + self.value + "\" for #" + str(self.image.id)
    else:
      return "Inactive solution \"" + self.value + "\" for #" + str(self.image.id)

class Resolution(models.Model):
  image = models.ForeignKey(Image, editable = False)
  user = models.ForeignKey(User, editable = False)
  solution = models.ForeignKey(Solution, null = True, editable = False)
  timestamp = models.DateTimeField(auto_now_add = True, editable = False)
  
  class Meta:
    unique_together = ("image", "user")
  
  def __unicode__(self):
    if self.solution:
      return self.user.username + " solved #" + str(self.image.id) + " on " + self.timestamp.strftime("%d.%m.%Y")
    else:
      return self.user.username + " gave up on #" + str(self.image.id) + " on " + self.timestamp.strftime("%d.%m.%Y")

class Comment(models.Model):
  image = models.ForeignKey(Image, editable = False)
  user = models.ForeignKey(User, editable = False)
  timestamp = models.DateTimeField(auto_now_add = True, editable = False)
  text = models.TextField()
  
  def __unicode__(self):
    return ("Comment by " + self.user.username + " for #" + str(self.image.id) + " on " + 
            self.timestamp.strftime("%d.%m.%Y %H:%M:%S") + ": " + self.text)
