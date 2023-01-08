from django.contrib import auth as djangoAuth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import paginator
from django import http, shortcuts
from django.views.decorators import http as httpDecorators

from wtp import auth, facebook, forms, halloffame, helper, image, models, openid, twitter, stats as wtpStats

@httpDecorators.require_POST
def changeFilter(request):
  """Changes the active filter."""
  if "filtermode" in request.POST and request.POST["filtermode"] in image.ImageNavigation.navTypes:
    request.session["filterMode"] = request.POST["filtermode"]
  
  return shortcuts.redirect("wtp.views.index")

@httpDecorators.require_GET
def facebookCallback(request):
  """Registers a link between a user's account and Facebook or registers/logins a user with Facebook."""
  if not "code" in request.GET:
    return http.HttpResponseBadRequest()
  
  accessToken = facebook.exchangeCodeForAccessToken(request.GET["code"])
  
  if accessToken:
    facebookId = facebook.getFacebookId(accessToken)
    
    if facebookId:
      if request.user.is_authenticated():
        facebook.enableFacebook(request.user, facebookId)
        return shortcuts.redirect("wtp.views.settings")
      else:
        if facebook.isUserRegistered(accessToken, facebookId):
          user = djangoAuth.authenticate(facebookId = facebookId)
          djangoAuth.login(request, user)
          
          return shortcuts.redirect("wtp.views.index")
        else:
          request.session["facebookRegistrationAccessToken"] = accessToken
          request.session["facebookRegistrationId"] = facebookId
          request.session["facebookRegistrationNickname"] = facebook.getNickname(accessToken)
          
          return shortcuts.redirect("wtp.views.facebookCompleteRegistration")
  
  return helper.renderTemplate(request, "facebook_failed.html")

def facebookCompleteRegistration(request):
  """Asks a user registering with Facebook to select his nickname and finally creates the user."""
  if request.method == "POST":
    form = forms.FacebookCompleteRegistrationForm(request.POST)
    if form.is_valid():
      facebook.registerFacebookUser(form)
      
      user = djangoAuth.authenticate(facebookId = form.cleaned_data["facebookId"])
      djangoAuth.login(request, user)
      
      return helper.renderTemplate(request, "register_successful.html")
  else:
    if (not "facebookRegistrationAccessToken" in request.session or
        not "facebookRegistrationNickname" in request.session):
      return helper.renderTemplate(request, "facebook_failed.html")
    
    facebookAccessToken = request.session["facebookRegistrationAccessToken"]
    facebookId = request.session["facebookRegistrationId"]
    facebookNickname = request.session["facebookRegistrationNickname"]
    
    del request.session["facebookRegistrationAccessToken"]
    del request.session["facebookRegistrationId"]
    del request.session["facebookRegistrationNickname"]
    
    form = forms.FacebookCompleteRegistrationForm({"facebookAccessToken": facebookAccessToken,
                                                   "facebookId": facebookId, "nickname": facebookNickname})
  
  return helper.renderTemplate(request, "facebook-completereg.html", {"form": form})

@httpDecorators.require_GET
def facebookConnect(request):
  """Redirects to the Facebook OAuth page to start the authorization process."""
  return shortcuts.redirect(facebook.getAuthStartUrl())

@login_required
@httpDecorators.require_POST
def facebookDisconnect(request):
  """Remove Facebook connection for a user."""
  facebook.disableFacebook(request.user)
  return shortcuts.redirect("wtp.views.settings")

@httpDecorators.require_GET
def faq(request):
  """Shows frequently asked questions page."""
  return helper.renderTemplate(request, "faq.html")

def forgotPassword(request):
  """Shows forgot password page or send forgotten password."""
  if request.method == "POST":
    form = forms.ForgotPasswordForm(request.POST)
    if form.is_valid():
      user = User.objects.get(username = form.cleaned_data["nickname"], email = form.cleaned_data["mailaddress"])
      auth.sendNewPassword(user)
      
      return helper.renderTemplate(request, "forgotpassword_successful.html")
  else:
    form = forms.ForgotPasswordForm()
  
  return helper.renderTemplate(request, "forgotpassword.html", {"form": form})

@httpDecorators.require_POST
def guess(request):
  """Handles a user's guess and marks the image as solved if the answer is correct."""
  form = forms.GuessForm(request.POST)
  if form.is_valid():
    imageObj = form.cleaned_data["image"]
    
    if imageObj.uploader != request.user:
      result = image.checkGuess(imageObj, form.cleaned_data["solution"])
      
      if result:
        if request.user.is_authenticated():
          if not imageObj.resolution_set.filter(user = request.user).exists():
            imageObj.resolution_set.create(user = request.user, solution = result)
            twitter.tweetImageSolved(request.user, imageObj)
        else:
          request.session["solved-" + str(imageObj.id)] = True
        
        return http.HttpResponse("right")
      else:
        return http.HttpResponse("wrong")
  
  return http.HttpResponseForbidden()

@httpDecorators.require_GET
def hallOfFame(request):
  """Shows hall of fame page."""
  topUploaders = halloffame.getHallOfFameTopUploaders()
  topSolvers = halloffame.getHallOfFameTopSolvers()
  topFirstSolvers = halloffame.getHallOfFameTopFirstSolvers()
  
  return helper.renderTemplate(request, "halloffame.html", {"topUploaders": topUploaders, "topSolvers": topSolvers,
                                                            "topFirstSolvers": topFirstSolvers})

@httpDecorators.require_GET
def hallOfFameDetail(request, pageType, page):
  """Shows a detailled hall of fame page for a specific category."""
  details = halloffame.getHallOfFameDetail(pageType)
  
  paginatorObj = paginator.Paginator(details["list"], 50)
  
  try:
    pageObj = paginatorObj.page(page)
  except paginator.EmptyPage:
    raise http.Http404()
  
  return helper.renderTemplate(request, "halloffame-detail.html",
                               {"title": details["title"], "pageType": pageType, "page": pageObj,
                                "data": {"table": pageObj.object_list, "average": details["average"]}})

@httpDecorators.require_GET
def imprint(request):
  """Shows imprint page."""
  return helper.renderTemplate(request, "imprint.html")

@httpDecorators.require_GET
def index(request):
  """Redirects to the active image. Selects a random image if none is active."""
  if not "filterMode" in request.session:
    request.session["filterMode"] = "All"
  
  if "curImage" in request.session:
    navClass = image.ImageNavigation(request.session["filterMode"], request.session["curImage"], request.user)
    if navClass.visible():
      curImage = models.Image.objects.get(pk = request.session["curImage"])
    else:
      curImage = navClass.random()
  else:
    curImage = None
  
  if not curImage:
    request.session["filterMode"] = "All"
    curImage = image.ImageNavigation("All", None, None).random()
  
  if curImage:
    return shortcuts.redirect("wtp.views.showImage", imageId = curImage.id)
  else:
    return shortcuts.redirect("wtp.views.upload")

def login(request):
  """Shows login page or logins a user and redirects to start page."""
  if request.method == "POST":
    form = forms.LoginForm(request.POST)
    if form.is_valid():
      user = djangoAuth.authenticate(username = form.cleaned_data["nickname"],
                                     password = form.cleaned_data["password"])
      djangoAuth.login(request, user)
      
      return shortcuts.redirect("wtp.views.index")
  else:
    form = forms.LoginForm()
  
  return helper.renderTemplate(request, "login.html", {"form": form})

@login_required
@httpDecorators.require_GET
def logout(request):
  """Terminates an user's session and redirects to start page."""
  djangoAuth.logout(request)
  
  return shortcuts.redirect("wtp.views.index")

@httpDecorators.require_GET
def mailConfirm(request, givenKey):
  """Confirms a mail address."""
  userProfiles = models.UserProfile.objects.filter(confirmKey = givenKey)
  if userProfiles:
    entry = userProfiles[0]
    
    entry.confirmKey = None
    entry.save()
    
    return helper.renderTemplate(request, "mailconfirm_successful.html")
  else:
    return helper.renderTemplate(request, "mailconfirm_failed.html")

def openIDCallback(request):
  """Registers a link between a user's account and an OpenID identity or registers/logins a user using an identity."""
  parameters = dict(request.GET.items())
  if request.method == "POST":
    parameters.update(request.POST.items())
  
  if not parameters:
    return http.HttpResponseBadRequest()
  
  result = openid.finishOpenIDAuth(request, parameters)
  
  if result:
    if request.user.is_authenticated():
      openid.enableOpenID(request.user, result["url"])
      return shortcuts.redirect("wtp.views.settings")
    else:
      if openid.isUserRegistered(result["url"]):
        user = djangoAuth.authenticate(openIDUrl = result["url"])
        djangoAuth.login(request, user)
        
        return shortcuts.redirect("wtp.views.index")
      else:
        request.session["openIDRegistrationUrl"] = result["url"]
        request.session["openIDRegistrationMailAddress"] = result["mailAddress"]
        
        return shortcuts.redirect("wtp.views.openIDCompleteRegistration")
  
  return helper.renderTemplate(request, "openid_failed.html")

def openIDCompleteRegistration(request):
  """Asks a user registering with OpenID to select his nickname and mail address and finally creates the user."""
  if not "openIDRegistrationUrl" in request.session:
      return helper.renderTemplate(request, "openid_failed.html")
  
  url = request.session["openIDRegistrationUrl"]
  
  if request.method == "POST":
    form = forms.OpenIDCompleteRegistrationForm(request.POST)
    if form.is_valid() and form.cleaned_data["url"] == url:  # Sanity check
      openid.registerOpenIDUser(form)
      
      user = djangoAuth.authenticate(openIDUrl = url)
      djangoAuth.login(request, user)
      
      return helper.renderTemplate(request, "register_successful.html")
  else:
    if not "openIDRegistrationMailAddress" in request.session:
      return helper.renderTemplate(request, "openid_failed.html")
    
    mailAddress = request.session["openIDRegistrationMailAddress"]
    del request.session["openIDRegistrationMailAddress"]
    
    form = forms.OpenIDCompleteRegistrationForm({"url": url, "nickname": mailAddress.split("@", 1)[0],
                                                 "mailaddress": mailAddress})
  
  return helper.renderTemplate(request, "openid-completereg.html", {"form": form})

@httpDecorators.require_GET
def openIDConnect(request):
  """Initiates the OpenID authentification process by contacting the provider and then redirecting the user to it."""
  if not "identity" in request.GET:
    return http.HttpResponseBadRequest()
  
  redirectUrl = openid.getAuthStartUrl(request, request.GET["identity"])
  
  if redirectUrl:
    return shortcuts.redirect(redirectUrl)
  else:
    return helper.renderTemplate(request, "openid_failed.html")

@login_required
@httpDecorators.require_POST
def openIDDisconnect(request):
  """Remove Twitter connection for a user."""
  form = forms.OpenIDDisableForm(request.POST)
  if form.is_valid():
    openid.disableOpenID(request.user, form.cleaned_data["url"])
    return shortcuts.redirect("wtp.views.settings")
  else:
    return http.HttpResponseBadRequest()

@httpDecorators.require_GET
def overview(request, navType, page):
  """Shows overview page."""
  allImages = image.ImageNavigation(navType, None, request.user).all()
  paginatorObj = paginator.Paginator(allImages, 32)
  
  try:
    pageObj = paginatorObj.page(page)
  except paginator.EmptyPage:
    raise http.Http404()
  
  rows = helper.tablify(image.addStatusToImageList(pageObj.object_list, request), 4)
  
  return helper.renderTemplate(request, "overview.html", {"navType": navType, "images": pageObj, "rows": rows})

@login_required
@httpDecorators.require_POST
def postComment(request):
  """Adds a comment to an image.."""
  form = forms.CommentForm(request.POST)
  if form.is_valid():
    image = form.cleaned_data["image"]
    
    if request.user == image.uploader or image.resolution_set.filter(user = request.user).exists():
      image.comment_set.create(user = request.user, text = form.cleaned_data["text"])
      
      return shortcuts.redirect("wtp.views.showImage", imageId = image.id)
  
  return http.HttpResponseForbidden()

def register(request):
  """Shows register page or handle register request."""
  if request.method == "POST":
    form = forms.RegisterForm(request.POST)
    if form.is_valid():
      auth.registerUser(form)
      
      user = djangoAuth.authenticate(username = form.cleaned_data["nickname"],
                                     password = form.cleaned_data["password1"])
      djangoAuth.login(request, user)
      
      return helper.renderTemplate(request, "register_successful.html")
  else:
    form = forms.RegisterForm()

  return helper.renderTemplate(request, "register.html", {"form": form})

def reportImage(request, imageId):
  """Shows the report image form or sends a mail to the admins."""
  imageObj = shortcuts.get_object_or_404(models.Image, pk = imageId, visible = True)
  
  if request.method == "POST":
    form = forms.ReportImageForm(request.POST)
    if form.is_valid():
      image.reportImage(imageObj.id, request.user.username if request.user.is_authenticated() else "Guest",
                        form.cleaned_data["text"])
      
      return helper.renderTemplate(request, "reportimage_successful.html")
  else:
    form = forms.ReportImageForm()
  
  return helper.renderTemplate(request, "reportimage.html", {"form": form, "image": imageObj})

@login_required
@httpDecorators.require_POST
def resolve(request):
  """Marks a user as having given up for an image and redirects back to the image."""
  form = forms.ResolveForm(request.POST)
  if form.is_valid():
    imageObj = form.cleaned_data["image"]
    
    if imageObj.uploader != request.user and not imageObj.resolution_set.filter(user = request.user).exists():
      imageObj.resolution_set.create(user = request.user)
      
      return shortcuts.redirect("wtp.views.showImage", imageId = imageObj.id)
  
  return http.HttpResponseForbidden()

@login_required
def settings(request):
  """Shows settings page if logged in (otherwise login page) or handle settings change."""
  userProfile = request.user.get_profile()
  openIDIdentities = openid.getOpenIDIdentities(request.user)
  hasFacebook = facebook.hasFacebook(request.user)
  hasTwitter = twitter.hasTwitter(request.user)
  
  if request.method == "POST":
    form = forms.ProfileForm(request.POST)
    if form.is_valid():
      auth.saveUserSettings(request.user, form)
  else:
    form = forms.ProfileForm({"mailaddress": request.user.email,
                              "showInHallOfFame": userProfile.showInHallOfFame,
                              "showAsFirstSolver": userProfile.showAsFirstSolver,
                              "showAsSolver": userProfile.showAsSolver,
                              "showPublicProfile": userProfile.showPublicProfile,
                              "twitterMessage": userProfile.twitterMessage,
                              "twitterAutoTweet": userProfile.twitterAutoTweet})
  
  return helper.renderTemplate(request, "settings.html", {"form": form, "openIDIdentities": openIDIdentities,
                                                          "hasFacebook": hasFacebook, "hasTwitter": hasTwitter, })

@httpDecorators.require_GET
def showImage(request, imageId):
  """Shows the requested image."""
  imageObj = shortcuts.get_object_or_404(models.Image, pk = imageId, visible = True)
  
  if not "viewed-" + str(imageObj.id) in request.session:
    image.increaseViewCount(imageObj)
  
  request.session["viewed-" + str(imageObj.id)] = True
  request.session["curImage"] = imageObj.id
  
  imageObj.status = image.getImageStatus(imageObj, request)
  solutions = ([obj.value for obj in imageObj.solution_set.filter(active = True)] if imageObj.status != "unsolved"
               else None)
  resolutions = imageObj.resolution_set.filter(solution__isnull = False).order_by("id")
  comments = imageObj.comment_set.order_by("-id")
  
  # TODO: This can be made better for sure
  firstsolver = None
  if resolutions:
    firstsolver = resolutions[0]
  
  if not "filterMode" in request.session:
    request.session["filterMode"] = "All"
  
  imageNav = image.ImageNavigation(request.session["filterMode"], imageObj.id, request.user)
  
  return helper.renderTemplate(request, "image.html", {"filterMode": request.session["filterMode"], "image": imageObj,
                                                       "imageNav": imageNav, "solutions": solutions,
                                                       "resolutions": resolutions, "comments": comments,
                                                       "firstsolver": firstsolver})

@httpDecorators.require_GET
def solvers(request, imageId):
  """Shows the solvers for the given image."""
  image = shortcuts.get_object_or_404(models.Image, pk = imageId, visible = True)
  resolutions = image.resolution_set.filter(solution__isnull = False).order_by("id")
  
  return helper.renderTemplate(request, "solvers.html", {"image": image, "resolutions": resolutions})

@httpDecorators.require_GET
def stats(request):
  """Shows statistics page."""
  statsObj = wtpStats.getStats()
  
  return helper.renderTemplate(request, "stats.html", {"stats": statsObj})

@httpDecorators.require_GET
def twitterCallback(request):
  """Registers a link between a user's account and Twitter or registers/logins a user with Twitter."""
  if not "oauth_token" in request.GET or not "oauth_verifier" in request.GET:
    return http.HttpResponseBadRequest()
  
  if "twitterRequestToken" in request.session:
    requestToken = request.session["twitterRequestToken"]
    del request.session["twitterRequestToken"]
    
    if requestToken[0] == request.GET["oauth_token"]:
      accessToken = twitter.exchangeVerifierForAccessToken(requestToken, request.GET["oauth_verifier"])
      
      if accessToken:
        if request.user.is_authenticated():
          twitter.enableTwitter(request.user, accessToken)
          return shortcuts.redirect("wtp.views.settings")
        else:
          if twitter.isUserRegistered(accessToken):
            user = djangoAuth.authenticate(twitterAccessKey = accessToken.key,
                                           twitterAccessSecret = accessToken.secret)
            djangoAuth.login(request, user)
            
            return shortcuts.redirect("wtp.views.index")
          else:
            request.session["twitterRegistrationAccessToken"] = accessToken
            request.session["twitterRegistrationNickname"] = twitter.getNickname(accessToken)
            
            return shortcuts.redirect("wtp.views.twitterCompleteRegistration")
  
  return helper.renderTemplate(request, "twitter_failed.html")

def twitterCompleteRegistration(request):
  """Asks a user registering with Twitter to select his nickname and finally creates the user."""
  if request.method == "POST":
    form = forms.TwitterCompleteRegistrationForm(request.POST)
    if form.is_valid():
      twitter.registerTwitterUser(form)
      
      user = djangoAuth.authenticate(twitterAccessKey = form.cleaned_data["twitterAccessKey"],
                                     twitterAccessSecret = form.cleaned_data["twitterAccessSecret"])
      djangoAuth.login(request, user)
      
      return helper.renderTemplate(request, "register_successful.html")
  else:
    if not "twitterRegistrationAccessToken" in request.session or not "twitterRegistrationNickname" in request.session:
      return helper.renderTemplate(request, "twitter_failed.html")
    
    twitterAccessToken = request.session["twitterRegistrationAccessToken"]
    twitterNickname = request.session["twitterRegistrationNickname"]
    
    del request.session["twitterRegistrationAccessToken"]
    del request.session["twitterRegistrationNickname"]
    
    form = forms.TwitterCompleteRegistrationForm({"twitterAccessKey": twitterAccessToken.key,
                                                  "twitterAccessSecret": twitterAccessToken.secret,
                                                  "nickname": twitterNickname})
  
  return helper.renderTemplate(request, "twitter-completereg.html", {"form": form})

@httpDecorators.require_GET
def twitterConnect(request):
  """Redirects to the Twitter OAuth page to start the authorization process."""
  result = twitter.startTwitterAuth()
  
  if result:
    request.session["twitterRequestToken"] = result["requestToken"]
    return shortcuts.redirect(result["url"])
  else:
    return helper.renderTemplate(request, "twitter_failed.html")

@login_required
@httpDecorators.require_POST
def twitterDisconnect(request):
  """Remove Twitter connection for a user."""
  twitter.disableTwitter(request.user)
  return shortcuts.redirect("wtp.views.settings")

@login_required
def upload(request):
  """Shows upload page or handle an upload with createImage."""
  if request.method == "POST":
    form = forms.UploadForm(request.POST, request.FILES)
    if form.is_valid():
      if image.createImage(request.user, form):
        return helper.renderTemplate(request, "upload_successful.html")
      else:
        return helper.renderTemplate(request, "upload_failed.html")
  else:
    form = forms.UploadForm()
  
  return helper.renderTemplate(request, "upload.html", {"form": form})

@httpDecorators.require_GET
def userProfile(request, userName):
  """Shows a user's profile page."""
  user = shortcuts.get_object_or_404(User, username = userName)
  
  if not user.get_profile().showPublicProfile:
    raise http.Http404()
  
  userProfile = wtpStats.getUserProfile(request, user)
  
  return helper.renderTemplate(request, "userprofile.html", {"userProfile": userProfile})
