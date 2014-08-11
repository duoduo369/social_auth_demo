from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^login-error', 'login_error', name='login_error'),
    url(r'^accounts/login', 'accounts_login', name='accounts_login'),

)
