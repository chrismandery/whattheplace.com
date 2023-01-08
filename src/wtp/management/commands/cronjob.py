import datetime
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
import fcntl

from wtp import models, stats, twitter

class Command(BaseCommand):
  help = "Runs various maintenance tasks."
  
  def handle(self, *args, **options):
    lockFile = open("/tmp/wtp-cron.lock", "w")
    fcntl.flock(lockFile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    
    try:
      pruneLimit = datetime.datetime.now() - datetime.timedelta(90)
      
      Session.objects.filter(expire_date__lt = datetime.datetime.now()).delete()
      models.PageHit.objects.filter(timestamp__lt = pruneLimit).delete()
      
      stats.buildTrafficDigests()
      twitter.sendActiveTweets()
    finally:
      fcntl.flock(lockFile, fcntl.LOCK_UN)
      lockFile.close()
