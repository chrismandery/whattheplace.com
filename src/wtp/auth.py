from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
from re import match

from wtp import helper, models

def registerUser(form):
  user = User.objects.create_user(form.cleaned_data["nickname"], form.cleaned_data["mailaddress"],
                                  form.cleaned_data["password1"])
  
  models.UserProfile.objects.create(user = user)
  
  if user.email:
    sendConfirmKey(user)

def saveUserSettings(user, form):
  if user.email != form.cleaned_data["mailaddress"]:
    user.email = form.cleaned_data["mailaddress"]
    changedMail = True
  else:
    changedMail = False
  
  if form.cleaned_data["password1"]:
    user.set_password(form.cleaned_data["password1"])
  
  user.save()
  
  userProfile = user.get_profile()
  userProfile.showInHallOfFame = form.cleaned_data["showInHallOfFame"]
  userProfile.showAsFirstSolver = form.cleaned_data["showAsFirstSolver"]
  userProfile.showAsSolver = form.cleaned_data["showAsSolver"]
  userProfile.showPublicProfile = form.cleaned_data["showPublicProfile"]
  userProfile.twitterMessage = form.cleaned_data["twitterMessage"]
  userProfile.twitterAutoTweet = form.cleaned_data["twitterAutoTweet"]
  userProfile.save()
  
  if changedMail and user.email:
    sendConfirmKey(user)

def sendConfirmKey(user):
  confirmKey = helper.generateAlNumString(40)
  
  helper.sendMail(user.email, "Please confirm your mail address", "mails/confirmmail.txt",
                  {"baseUrl": settings.BASE_URL, "confirmKey": confirmKey})
  
  userProfile = user.get_profile()
  userProfile.confirmKey = confirmKey
  userProfile.save()

def sendNewPassword(user):
  newPassword = helper.generateAlNumString(8)
  
  helper.sendMail(user.email, "New password", "mails/newpassword.txt", {"newPassword": newPassword})
  
  user.set_password(newPassword)
  user.save()

def validateNickname(nickname):
  if User.objects.filter(username = nickname).exists():
    raise ValidationError("Nick name already exists.")
  
  if not match("^(\w|_)+$", nickname):
    raise ValidationError("Nick name may only contain alphanumeric characters and underscore.")
  
  return nickname
