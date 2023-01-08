from django import template

register = template.Library()

@register.filter("truncate")  
def truncate(value, length):  
  if len(value) <= length:  
    return value  
  
  return value[:length] + "..."   
