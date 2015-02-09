from django.conf.urls import patterns, url

urlpatterns = patterns('Inventar.views',
	url(r'^$', 'index'),
	url(r'^info/(?P<id>\d+)/$', 'info'),
	url(r'^filter/', 'filter_view'),
	url(r'^add/', 'add'),
	url(r'^remove/', 'remove'),
	url(r'^create/', 'create'),
	url(r'^addType/', 'addType'),
	url(r'^edit/(?P<id>\d+)/$', 'edit'),
)
