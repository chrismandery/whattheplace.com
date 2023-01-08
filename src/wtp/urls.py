from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns("wtp.views",
  ("^$", "index"),
  ("^ChangeFilter/$", "changeFilter"),
  ("^FacebookCallback/", "facebookCallback"),
  ("^FacebookCompleteRegistration/$", "facebookCompleteRegistration"),
  ("^FacebookConnect/", "facebookConnect"),
  ("^FacebookDisconnect/", "facebookDisconnect"),
  ("^FAQ/$", "faq"),
  ("^ForgotPassword/$", "forgotPassword"),
  ("^Guess/$", "guess"),
  ("^HallOfFame/$", "hallOfFame"),
  ("^HallOfFame/(?P<pageType>(TopUploaders|TopSolvers|TopFirstSolvers))/(?P<page>\d+)/$", "hallOfFameDetail"),
  ("^Imprint/$", "imprint"),
  ("^Login/$", "login"),
  ("^Logout/$", "logout"),
  ("^MailConfirm/(?P<givenKey>\w{40})/$", "mailConfirm"),
  ("^OpenIDCallback/", "openIDCallback"),
  ("^OpenIDCompleteRegistration/$", "openIDCompleteRegistration"),
  ("^OpenIDConnect/", "openIDConnect"),
  ("^OpenIDDisconnect/", "openIDDisconnect"),
  ("^Overview/(?P<navType>(All|Own|Solvable|Solved|Unsolved|UnsolvedByMe|GaveUp))/(?P<page>\d+)/$", "overview"),
  ("^PostComment/$", "postComment"),
  ("^Register/$", "register"),
  ("^ReportImage/(?P<imageId>\d+)/$", "reportImage"),
  ("^Resolve/$", "resolve"),
  ("^Settings/$", "settings"),
  ("^Show/(?P<imageId>\d+)/$", "showImage"),
  ("^Solvers/(?P<imageId>\d+)/$", "solvers"),
  ("^Stats/$", "stats"),
  ("^TwitterCallback/", "twitterCallback"),
  ("^TwitterCompleteRegistration/$", "twitterCompleteRegistration"),
  ("^TwitterConnect/", "twitterConnect"),
  ("^TwitterDisconnect/", "twitterDisconnect"),
  ("^Upload/$", "upload"),
  ("^UserProfile/(?P<userName>(\w|_)+)/$", "userProfile")
)

urlpatterns += patterns("",
  url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^', include('debug_toolbar_htmltidy.urls'))
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
