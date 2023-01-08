from django.conf import settings
from django.db import IntegrityError
from django.db.models import F
from hashlib import md5
from PIL import Image as PILImage
from shutil import copyfile
from tempfile import mkstemp
import os

from wtp import helper, models

class ImageNavigation():
  navTypes = ["All", "Own", "Solvable", "Solved", "Unsolved", "UnsolvedByMe", "GaveUp"]
  
  def __init__(self, navType, curImage, user):
    if navType == "All":
      self.querySet = models.Image.objects.filter(visible = True)
    
    elif navType == "Own" and user.is_authenticated():
      self.querySet = models.Image.objects.filter(visible = True, uploader = user) 
    
    elif navType == "Solvable" and user.is_authenticated():
      self.querySet = (models.Image.objects.filter(visible = True).exclude(uploader = user).
                       exclude(resolution__user = user))
    
    elif navType == "Solved" and user.is_authenticated():
      self.querySet = models.Image.objects.filter(visible = True, resolution__user = user,
                                                  resolution__solution__isnull = False)
    
    elif navType == "Unsolved":
      self.querySet = models.Image.objects.filter(visible = True).exclude(resolution__solution__isnull = False)
    
    elif navType == "UnsolvedByMe" and user.is_authenticated():
      self.querySet = models.Image.objects.filter(visible = True).exclude(resolution__user = user)
    
    elif navType == "GaveUp" and user.is_authenticated():
      self.querySet = models.Image.objects.filter(visible = True, resolution__user = user,
                                                  resolution__solution__isnull = True)
    
    else:
      self.querySet = models.Image.objects.none()
    
    self.curImage = curImage
  
  def all(self):
    return self.querySet
  
  def first(self):
    # TODO
    qs = self.querySet.order_by("id")
    first = qs[0] if qs.count() else None
    return None if first.id == self.curImage else first
  
  def last(self):
    # TODO
    qs = self.querySet.order_by("-id")
    last = qs[0] if qs.count() else None
    return None if last.id == self.curImage else last
  
  def next(self):
    qs = self.querySet.filter(id__gt = self.curImage).order_by("id")
    return qs[0] if qs.count() else None
  
  def prev(self):
    qs = self.querySet.filter(id__lt = self.curImage).order_by("-id")
    return qs[0] if qs.count() else None
  
  def random(self):
    qs = self.querySet.exclude(pk = self.curImage).order_by("?")
    return qs[0] if qs.count() else None
  
  def visible(self):
    return self.querySet.filter(pk = self.curImage).exists()

def addStatusToImageList(imageList, request):
  for image in imageList:
    image.status = getImageStatus(image, request)
  
  return imageList

def checkGuess(image, guess):
  for possibleSolution in image.solution_set.filter(active = True):
    if helper.normalizeSolution(guess) == possibleSolution.value:
      return possibleSolution

def createImage(user, form):
  image = form.cleaned_data["image"]
  
  # Save upload image temporary and hash it
  imageHashObj = md5()
  tmpHandle, tmpPath = mkstemp(".jpeg")
  
  for chunk in image.chunks():
    os.write(tmpHandle, chunk)
    imageHashObj.update(chunk)
  
  os.close(tmpHandle)
  uploadedImageHash = imageHashObj.hexdigest()
  
  # Create image in database
  image = models.Image(imageHash = uploadedImageHash,
                       visible = False,
                       uploader = user,
                       hint = form.cleaned_data["hint"],
                       license = form.cleaned_data["license"],
                       author = form.cleaned_data["author"],
                       source = form.cleaned_data["source"],
                       views = 0)
  try:
    image.save()
  except IntegrityError:
    # Image already in database
    return False
  
  # Save original
  copyfile(tmpPath, os.path.join(settings.MEDIA_ROOT, "orig", uploadedImageHash + ".jpeg"))
  
  # Open image, resize for display and save
  pilImage = PILImage.open(tmpPath)
  pilImage.thumbnail((600, 600), PILImage.ANTIALIAS)
  pilImage.save(os.path.join(settings.MEDIA_ROOT, "images", uploadedImageHash + ".jpeg"))
  
  # Open image, resize for thumbnail and save
  pilImage = PILImage.open(tmpPath)
  pilImage.thumbnail((160, 160), PILImage.ANTIALIAS)
  pilImage.save(os.path.join(settings.MEDIA_ROOT, "thumbs", uploadedImageHash + ".jpeg"))
  
  # Save solutions
  solutions = form.cleaned_data["solution"].replace(",", ";")
  for solution in solutions.split(";"):
    image.solution_set.create(value = helper.normalizeSolution(solution), active = True)
  
  # Create comment if available
  if form.cleaned_data["comment"]:
    image.comment_set.create(image = image, user = user, text = form.cleaned_data["comment"])
  
  # Send notification mail to admin
  helper.sendMail(settings.ADMINS[0][1], "New image", "mails/newimage.txt", {"username": user.username})
  
  return True

def getImageStatus(image, request):
  if request.user.is_authenticated():
    if image.uploader == request.user:
      return "OwnImage"
    else:
      resolutions = image.resolution_set.filter(user = request.user)
      if resolutions:
        resolution = resolutions[0]
        if resolution.solution:
          return "SolvedIt"
        else:
          return "GaveUp"
      else:
        return "Unsolved"
  else:
    if "solved-" + str(image.id) in request.session:
      return "SolvedIt"
    else:
      return "Unsolved"

def increaseViewCount(image):
  models.Image.objects.filter(pk = image.id).update(views = F("views") + 1)
  image.views += 1

def reportImage(imageId, username, reason):
  helper.sendMail(settings.ADMINS[0][1], "Image reported", "mails/reportimage.txt",
                  {"imageId": imageId, "username": username, "reason": reason})
