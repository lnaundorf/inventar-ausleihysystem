from django.conf.urls import patterns, url

urlpatterns = patterns('Public.views',
	url(r'^$', 'index'),
	url(r'^inventar', 'public_inventar'),
)
