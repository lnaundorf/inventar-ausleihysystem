from django.conf.urls import patterns, include, url

urlpatterns = patterns('Benutzer.views',
	url(r'^$', 'index'),
	url(r'^info/(?P<id>\d+)/', 'info'),
	url(r'^filter/', 'filter_view'),
	url(r'^getUser/', 'get_user'),
	url(r'^add/', 'add'),
	url(r'^remove/', 'remove'),
	url(r'^create', 'create_user'),
	url(r'^edit/(?P<id>\d+)/', 'edit'),
)
