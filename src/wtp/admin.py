from django.contrib import admin

from wtp import models

class CommentAdmin(admin.ModelAdmin):
  date_hierarchy = "timestamp"
  list_display = ("timestamp", "user", "image", "text")

class ImageAdmin(admin.ModelAdmin):
  date_hierarchy = "dateAdded"
  list_display = ("visible", "id", "uploader", "thumbImage", "solutions", "hint", "copyright",
                  "dateAdded", "views")

class ResolutionAdmin(admin.ModelAdmin):
  date_hierarchy = "timestamp"

class SolutionAdmin(admin.ModelAdmin):
  list_display = ("active", "image", "value")
  list_filter = ("image",)

admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.License)
admin.site.register(models.OpenIDAssociation)
admin.site.register(models.OpenIDNonce)
admin.site.register(models.PageHit)
admin.site.register(models.Resolution, ResolutionAdmin)
admin.site.register(models.SentMail)
admin.site.register(models.Solution, SolutionAdmin)
admin.site.register(models.TrafficDigest)
admin.site.register(models.Tweet)
admin.site.register(models.UserOpenID)
admin.site.register(models.UserProfile)
