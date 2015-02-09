from django.conf.urls import patterns, url

urlpatterns = patterns('Dashboard.views',
	url(r'^$', 'index'),
)
