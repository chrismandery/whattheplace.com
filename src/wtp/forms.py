from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import os
from PIL.Image import open
from tempfile import mkstemp

from wtp import auth, facebook, models, twitter

class CommentForm(forms.Form):
  image = forms.ModelChoiceField(queryset = models.Image.objects.filter(visible = True))
  text = forms.CharField()

class FacebookCompleteRegistrationForm(forms.Form):
  facebookAccessToken = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
  facebookId = forms.IntegerField(widget = forms.HiddenInput(), min_value = 1)
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  mailaddress = forms.EmailField(label = "Mail address (optional)", required = False, max_length = 80)
  
  def clean(self):
    if facebook.getFacebookId(self.cleaned_data["facebookAccessToken"]) != str(self.cleaned_data["facebookId"]):
      raise forms.ValidationError("Facebook access not valid.")
    
    return self.cleaned_data
  
  def clean_nickname(self):
    return auth.validateNickname(self.cleaned_data["nickname"])

class ForgotPasswordForm(forms.Form):
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  mailaddress = forms.EmailField(label = "Mail address", max_length = 80)
  
  def clean(self):
    try:
      user = User.objects.get(username = self.cleaned_data.get("nickname"),
                              email = self.cleaned_data.get("mailaddress"))
    except User.DoesNotExist:
      raise forms.ValidationError("Invalid nick name or mail address.")
    
    if not user.is_active:
      raise forms.ValidationError("User is disabled.")
    
    if user.get_profile().confirmKey:
      raise forms.ValidationError("Mail address has not been confirmed.")
    
    return self.cleaned_data

class GuessForm(forms.Form):
  image = forms.ModelChoiceField(queryset = models.Image.objects.filter(visible = True))
  solution = forms.CharField()

class LoginForm(forms.Form):
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  password = forms.CharField(label = "Password", widget = forms.PasswordInput(), max_length = 40)
  
  def clean(self):
    user = authenticate(username = self.cleaned_data.get("nickname"),
                        password = self.cleaned_data.get("password"))
    
    if user is None or not user.is_active:
      raise forms.ValidationError("Login failed.")
    
    return self.cleaned_data

class OpenIDCompleteRegistrationForm(forms.Form):
  url = forms.URLField(widget = forms.HiddenInput(), max_length = 200)
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  mailaddress = forms.EmailField(label = "Mail address (optional)", required = False, max_length = 80)
  
  def clean_nickname(self):
    return auth.validateNickname(self.cleaned_data["nickname"])

class OpenIDDisableForm(forms.Form):
  url = forms.URLField()
  
class ProfileForm(forms.Form):
  password1 = forms.CharField(label = "Password", required = False, widget = forms.PasswordInput(),
                              max_length = 40)
  password2 = forms.CharField(label = "Password (repeat)", required = False, widget = forms.PasswordInput(),
                              max_length = 40)
  mailaddress = forms.EmailField(label = "Mail address", help_text = "If you change the mail address, you will be " + 
                                 "mailed a link to confirm your mail address", required = False, max_length = 80)
  showInHallOfFame = forms.BooleanField(label = "Show in Hall of Fame", help_text = "Specify whether you want you " + 
                                        "username to be shown on the Hall of Fame page with your score.",
                                        required = False)
  showAsFirstSolver = forms.BooleanField(label = "Show as first solver", help_text = "Specify whether your username " + 
                                         "shall be shown on the main page below the images that have been solved " + 
                                         "first by you.", required = False)
  showAsSolver = forms.BooleanField(label = "Show me on solvers page", help_text = "Specify whether you want to be " + 
                                    "shown in a list of a people that solved a certain image.", required = False)
  showPublicProfile = forms.BooleanField(label = "Show player profile", help_text = "Specify whether you want a " + 
                                         "public profile page, containing the images you uploaded, solved, commented " + 
                                         "or gave up on. Of course, your profile does not include your mail address, " + 
                                         "as \"What the Place?\" strictly respects your privacy.", required = False)
  twitterMessage = forms.CharField(label = "Twitter message", help_text = "Text to be twittered (leave empty for " + 
                                   "default). You can use %ID% for the id of the image and %URL% for the URL to the " + 
                                   "image.", required = False, max_length = 140)
  twitterAutoTweet = forms.BooleanField(label = "Auto-Tweet", help_text = "If enabled, post tweet when an image has " + 
                                        "been solved.", required = False)
  
  def clean(self):
    if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
      raise forms.ValidationError("Passwords are not the same.")
    
    return self.cleaned_data

class RegisterForm(forms.Form):
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  password1 = forms.CharField(label = "Password", widget = forms.PasswordInput(), max_length = 40)
  password2 = forms.CharField(label = "Password (repeat)", widget = forms.PasswordInput(), max_length = 40)
  mailaddress = forms.EmailField(label = "Mail address (optional)", required = False, max_length = 80)
  
  def clean(self):
    if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
      raise forms.ValidationError("Passwords are not the same.");
    
    return self.cleaned_data
  
  def clean_nickname(self):
    return auth.validateNickname(self.cleaned_data["nickname"])

class ReportImageForm(forms.Form):
  text = forms.CharField(label = "Message")

class ResolveForm(forms.Form):
  image = forms.ModelChoiceField(queryset = models.Image.objects.filter(visible = True))

class TwitterCompleteRegistrationForm(forms.Form):
  twitterAccessKey = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
  twitterAccessSecret = forms.CharField(widget = forms.HiddenInput(), max_length = 255)
  nickname = forms.CharField(label = "Nick name", max_length = 20)
  mailaddress = forms.EmailField(label = "Mail address (optional)", required = False, max_length = 80)
  
  def clean(self):
    if not twitter.checkTwitterAccess(self.cleaned_data["twitterAccessKey"], self.cleaned_data["twitterAccessSecret"]):
      raise forms.ValidationError("Twitter access not valid.");
    
    return self.cleaned_data
  
  def clean_nickname(self):
    return auth.validateNickname(self.cleaned_data["nickname"])

class UploadForm(forms.Form):
  image = forms.ImageField(label = "Image", help_text = "Allowed: JPEG, max. 5MB, min. 600px width or 600px height, " + 
                           "aspect ratio between 1:2 and 2:1")
  solution = forms.CharField(label = "Solution", help_text = "Case-insensitive, no need to \"transcribe\" German " + 
                             "umlauts, separate multiple possibilities with comma or semicolon.")
  license = forms.ModelChoiceField(label = "License", help_text = "When submitting images not made by yourself, " + 
                                   "please provide an URL in the next field that can be used to verify the license.",
                                   queryset = models.License.objects.filter(visible = True))
  source = forms.URLField(label = "Source (URL)", help_text = "Provide a URL to your source of the picture, e.g. a " + 
                           "Wikipedia page. This link is visible only for solvers of your image or user who gave up. " + 
                           "Optional, but recommended.", required = False)
  author = forms.CharField(label = "Author", help_text = "Name of photographer/author of the image. This field is " + 
                           "required for attribution licenses like Creative Commons but appreciated for every image.",
                           required = False)
  hint = forms.CharField(label = "Hint", help_text = "Hint for this image that will be shown as a tooltip. Can be " + 
                         "used to specifiy something like \"country name is also possible\".", required = False)
  comment = forms.CharField(label = "Comment", help_text = "Optional first comment to post to the image. Comments " + 
                            "are visible only for solvers of your image or user who gave up.", required = False)
  
  def clean_image(self):
    image = self.cleaned_data["image"]
    
    if image.size > 5 * 1024 * 1024:
      raise forms.ValidationError("File larger than 5MB.")
    
    if image.content_type != "image/jpeg":
      raise forms.ValidationError("Not in JPEG format.")
    
    # Save image to open it with PIL
    tmpHandle, tmpPath = mkstemp(".jpeg")
    for chunk in image.chunks():
      os.write(tmpHandle, chunk)
    os.close(tmpHandle)
    
    pilImage = open(tmpPath)
    width, height = pilImage.size
    
    if width < 600 and height < 600:
      raise forms.ValidationError("Must have at least a width or a height of 600 pixels.")
    
    if width > 2 * height or height > 2 * width:
      raise forms.ValidationError("Must have aspect ratio between 1:2 and 2:1.")
    
    return image
