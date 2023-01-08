from __future__ import division
from django.contrib.auth.models import User
from django.db.models import Count

from wtp import models

def getHallOfFameDetail(pageType):
  if pageType == "TopUploaders":
    title = "Top Uploaders"
    list = getTopUploaders()
    average = getTopUploadersAverage()
  
  elif pageType == "TopSolvers":
    title = "Top Solvers"
    list = getTopSolvers()
    average = getTopSolversAverage()
  
  else:
    title = "Top First Solvers"
    list = getTopFirstSolvers()
    average = getTopFirstSolversAverage()
  
  return {"title": title, "list": list, "average": average}

def getHallOfFameTopFirstSolvers():
  return {"type": "TopFirstSolvers", "table": getTopFirstSolvers()[0:10], "average": getTopFirstSolversAverage()}

def getHallOfFameTopSolvers():
  return {"type": "TopSolvers", "table": getTopSolvers()[0:10], "average": getTopSolversAverage()}

def getHallOfFameTopUploaders():
  return {"type": "TopUploaders", "table": getTopUploaders()[0:10], "average": getTopUploadersAverage()}

def getTopFirstSolvers():
  firstResolutionIds = []
  for image in models.Image.objects.filter(visible = True):
    resolutions = image.resolution_set.filter(solution__isnull = False).order_by("id")
    if resolutions:
      firstResolutionIds.append(resolutions[0].id)
  
  topFirstSolvers = (models.Resolution.objects.filter(id__in = firstResolutionIds).values("user").
                     annotate(count = Count("id")).order_by("-count"))
  for topFirstSolver in topFirstSolvers:
    topFirstSolver["user"] = User.objects.get(pk = topFirstSolver["user"])
  
  return topFirstSolvers

def getTopFirstSolversAverage():
  return (models.Resolution.objects.filter(solution__isnull = False).values("image").distinct().count() / 
          User.objects.count())

def getTopSolvers():
  topSolvers = (models.Resolution.objects.filter(solution__isnull = False).values("user").annotate(count = Count("id")).
                order_by("-count"))
  
  for topSolver in topSolvers:
    topSolver["user"] = User.objects.get(pk = topSolver["user"])

  return topSolvers

def getTopSolversAverage():
  return models.Resolution.objects.filter(solution__isnull = False).count() / User.objects.count()

def getTopUploaders():
  topUploaders = (models.Image.objects.filter(visible = True).values("uploader").annotate(count = Count("id")).
                  order_by("-count"))
  
  for topUploader in topUploaders:
    topUploader["user"] = User.objects.get(pk = topUploader["uploader"])

  return topUploaders

def getTopUploadersAverage():
  return models.Image.objects.filter(visible = True).count() / User.objects.count()
