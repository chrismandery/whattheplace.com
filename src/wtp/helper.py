from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django import template
from random import choice
import string

from wtp.models import Image, SentMail

def generateAlNumString(length):
  return "".join([choice(string.letters + string.digits) for i in range(length)]) #@UnusedVariable

def normalizeSolution(s):
  s = s.lower().strip()
  
  s = s.replace(u"\xe4", "ae")
  s = s.replace(u"\xf6", "oe")
  s = s.replace(u"\xfc", "ue")
  s = s.replace(u"\xdf", "ss")
  
  return s

def renderTemplate(request, templateName, context = {}):
  requestContext = template.RequestContext(request)
  requestContext["user"] = request.user
  
  if request.user.is_authenticated():
    requestContext["userSolvedCount"] = Image.objects.filter(visible = True, resolution__user = request.user,
                                                             resolution__solution__isnull = False).count()
    requestContext["userSolvableCount"] = Image.objects.filter(visible = True).exclude(uploader = request.user).count()
  
  return render_to_response(templateName, context, requestContext)

def sendMail(recipient, subject, templateName, contextDict):
  text = template.loader.get_template(templateName).render(template.Context(contextDict))
  
  send_mail("[What The Place?] " + subject, text, settings.SERVER_EMAIL, [recipient])
  
  SentMail.objects.create(recipient = recipient, subject = subject, text = text)

def tablify(input, numCols):
  rows = []
  
  while input:
    row = input[0:numCols]
    
    if len(input) < numCols:
      row.extend(["filler" for i in range(numCols - len(input))]) #@UnusedVariable
    
    rows.append(row)
    input = input[numCols:]
  
  return rows
