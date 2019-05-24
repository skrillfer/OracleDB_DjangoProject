from django.conf.urls import  patterns, include, url
#from django.conf.urls.defaults import *
#from django.views.generic import list_detail
from django.contrib import admin
from python_hol.models import Cliente

admin.autodiscover()

urlpatterns = patterns('',
 
    url(r'^',include("python_hol.urls")),
    url(r'^admin/', include(admin.site.urls)),
)

