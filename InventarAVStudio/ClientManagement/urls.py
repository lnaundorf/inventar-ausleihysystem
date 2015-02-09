from django.conf.urls import patterns, url

urlpatterns = patterns('ClientManagement.views',
	url(r'^$', 'index'),
	url(r'^computer/edit/(?P<id>\d+)/$', 'computer_edit'),
	url(r'^computer/create/$', 'computer_create'),
	url(r'^type/edit/(?P<id>\d+)/$', 'type_edit'),
	url(r'^type/create/$', 'type_create'),
	url(r'^key/edit/(?P<id>\d+)/$', 'key_edit'),
	url(r'^key/create/$', 'key_create'),
	url(r'^dhcp/$', 'dhcp_config'),
)
