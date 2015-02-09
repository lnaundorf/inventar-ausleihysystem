from django.conf.urls import patterns, url

urlpatterns = patterns('Schein.views',
	url(r'^$', 'index'),
	url(r'^info/(?P<schein_id>\d+)/$', 'info'),
	url(r'^erstellen/$', 'erstellen'),
	url(r'^download', 'download'),
	url(r'^issue', 'issue'),
	url(r'^(?P<typ>\w+)/filter', 'filter_view'),
	url(r'^edit/(?P<id>\d+)/', 'edit'),
)
