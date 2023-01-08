import datetime
from django.conf import settings

from wtp import helper, image, models

def buildTrafficDigest(start, end, hour, minRequestsForMail):
  requests = models.PageHit.objects.filter(timestamp__gte = start, timestamp__lt = end).count()
  sessions = (models.PageHit.objects.filter(timestamp__gte = start, timestamp__lt = end).values("sessionKey").
              distinct().count())
  users = models.User.objects.filter(date_joined__gte = start, date_joined__lt = end).count()
  resolutions = models.Resolution.objects.filter(timestamp__gte = start, timestamp__lt = end).count()
  comments = models.Comment.objects.filter(timestamp__gte = start, timestamp__lt = end).count()
  
  digest = {"start": start, "end": end, "requests": requests, "sessions": sessions, "users": users,
            "resolutions": resolutions, "comments": comments}
  
  models.TrafficDigest.objects.create(date = start.date(), hour = hour, requests = digest["requests"],
                                      sessions = digest["sessions"], users = digest["users"],
                                      resolutions = digest["resolutions"], comments = digest["comments"])
  if digest["requests"] >= minRequestsForMail:
    sendTrafficDigest(digest)

def buildTrafficDigests():
  end = datetime.datetime.now().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
  start = end - datetime.timedelta(days = 1)
  
  if not models.TrafficDigest.objects.filter(date = start.date(), hour = None).exists():
    buildTrafficDigest(start, end, None, 0)
  
  end = datetime.datetime.now().replace(minute = 0, second = 0, microsecond = 0)
  start = end - datetime.timedelta(hours = 1)
  
  if not models.TrafficDigest.objects.filter(date = start.date(), hour = start.hour).exists():
    buildTrafficDigest(start, end, start.hour, 200)

def getStats():
  stats1 = []
  stats2 = []
  
  ago1d = datetime.datetime.now() - datetime.timedelta(1)
  ago7d = datetime.datetime.now() - datetime.timedelta(7)
  ago30d = datetime.datetime.now() - datetime.timedelta(30)
  
  baseQuery = models.Image.objects.filter(visible = True)
  subStats = {"name": "Images",
              "total": baseQuery.count(),
              "1d": baseQuery.filter(dateAdded__gte = ago1d).count(),
              "7d": baseQuery.filter(dateAdded__gte = ago7d).count(),
              "30d": baseQuery.filter(dateAdded__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.Comment.objects
  subStats = {"name": "Comments",
              "total": baseQuery.count(),
              "1d": baseQuery.filter(timestamp__gte = ago1d).count(),
              "7d": baseQuery.filter(timestamp__gte = ago7d).count(),
              "30d": baseQuery.filter(timestamp__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.Resolution.objects.filter(solution__isnull = False)
  subStats = {"name": "Correct solutions given",
              "total": baseQuery.count(),
              "1d": baseQuery.filter(timestamp__gte = ago1d).count(),
              "7d": baseQuery.filter(timestamp__gte = ago7d).count(),
              "30d": baseQuery.filter(timestamp__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.Resolution.objects.filter(solution__isnull = True)
  subStats = {"name": "Solutions requested (given up)",
              "total": baseQuery.count(),
              "1d": baseQuery.filter(timestamp__gte = ago1d).count(),
              "7d": baseQuery.filter(timestamp__gte = ago7d).count(),
              "30d": baseQuery.filter(timestamp__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.User.objects
  subStats = {"name": "Registered users",
              "total": baseQuery.count(),
              "1d": baseQuery.filter(date_joined__gte = ago1d).count(),
              "7d": baseQuery.filter(date_joined__gte = ago7d).count(),
              "30d": baseQuery.filter(date_joined__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.PageHit.objects
  subStats = {"name": "Requests",
              "total":-1,
              "1d": baseQuery.filter(timestamp__gte = ago1d).count(),
              "7d": baseQuery.filter(timestamp__gte = ago7d).count(),
              "30d": baseQuery.filter(timestamp__gte = ago30d).count()}
  stats1.append(subStats)
  
  baseQuery = models.PageHit.objects.values("sessionKey").distinct()
  subStats = {"name": "Sessions",
              "total":-1,
              "1d": baseQuery.filter(timestamp__gte = ago1d).count(),
              "7d": baseQuery.filter(timestamp__gte = ago7d).count(),
              "30d": baseQuery.filter(timestamp__gte = ago30d).count()}
  stats1.append(subStats)
  
  subStats = {"name": "Images awaiting activation",
              "value": models.Image.objects.filter(visible = False).count()}
  stats2.append(subStats)
  
  return {"stats1": stats1, "stats2": stats2}

def getUserProfile(request, user):
  userProfile = {}
  
  userProfile["username"] = user.username
  
  list = image.addStatusToImageList(models.Image.objects.filter(visible = True, uploader = user).order_by("id"),
                                    request)
  userProfile["uploaded"] = helper.tablify(list, 4)
  userProfile["uploadedCount"] = len(list)
  
  list = image.addStatusToImageList(models.Image.objects.filter(visible = True, resolution__user = user,
                                                                resolution__solution__isnull = False).order_by("id"),
                                                                request)
  userProfile["solved"] = helper.tablify(list, 4)
  userProfile["solvedCount"] = len(list)
  
  list = image.addStatusToImageList(models.Image.objects.filter(visible = True, resolution__user = user,
                                                                resolution__solution__isnull = True).order_by("id"),
                                                                request)
  userProfile["gaveUp"] = helper.tablify(list, 4)
  userProfile["gaveUpCount"] = len(list)
  
  list = image.addStatusToImageList(models.Image.objects.filter(visible = True, comment__user = user).order_by("id"),
                                    request)
  userProfile["commented"] = helper.tablify(list, 4)
  userProfile["commentedCount"] = len(list)
  
  return userProfile

def sendTrafficDigest(digest):
  subject = "Traffic digest: " + str(digest["requests"]) + " requests, " + str(digest["sessions"]) + " sessions"
  
  if (digest["users"]):
    subject += ", " + str(digest["users"]) + " users"
  
  if (digest["resolutions"]):
    subject += ", " + str(digest["resolutions"]) + " resolutions"
  
  if (digest["comments"]):
    subject += ", " + str(digest["comments"]) + " comments"
  
  helper.sendMail(settings.ADMINS[0][1], subject, "mails/trafficdigest.txt", {"digest": digest})
