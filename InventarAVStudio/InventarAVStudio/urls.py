from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^$', 'Inventar.views.login_or_index'),
	url(r'^inventar/', include('Inventar.urls')),
	url(r'^benutzer/', include('Benutzer.urls')),
	url(r'^schein/', include('Schein.urls')),
	url(r'^public/', include('Public.urls')),
	url(r'^dashboard/', include('Dashboard.urls')),
	url(r'^pool/', include('ClientManagement.urls')),
	url(r'^logout/$', 'Inventar.views.logout_view'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
