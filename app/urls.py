from django.conf.urls.defaults import patterns, url, include
from app.views import index

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
)
