from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fanfan.views.home', name='home'),
    # url(r'^fanfan/', include('fanfan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^pia/fanfan/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^pia/fanfan/admin/', include(admin.site.urls)),
)

urlpatterns += patterns('gao.views',
    url(r'^pia/fanfan/$', 'index'),
    url(r'^pia/fanfan/gao/$', 'index'),
    url(r'^pia/fanfan/gao/list/(?P<good_name>[^/]*)/$', 'list'),
    url(r'^pia/fanfan/gao/register/$', 'register'),
    url(r'^pia/fanfan/gao/login/$', 'login_'),
    url(r'^pia/fanfan/gao/logout/$', 'logout_'),
    url(r'^pia/fanfan/gao/profile/$', 'profile'),
    url(r'^pia/fanfan/gao/book/$', 'book'),
    url(r'^pia/fanfan/gao/unbook/$', 'unbook'),
    url(r'^pia/fanfan/gao/transfer/$', 'transfer'),
)

urlpatterns += patterns('',
	url(r'pia/fanfan/static/admin/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/'}),
)
