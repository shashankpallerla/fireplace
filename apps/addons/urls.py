from django.conf.urls.defaults import patterns, url, include
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from . import views

ADDON_ID = r"""(?P<addon_id>[^/<>"']+)"""


# These will all start with /addon/<addon_id>/
detail_patterns = patterns('',
    url('^$', views.addon_detail, name='addons.detail'),
    url('^eula/(?P<file_id>\d+)?$', views.eula, name='addons.eula'),
    url('^license/(?P<version>[^/]+)?', views.license, name='addons.license'),
    url('^privacy/', views.privacy, name='addons.privacy'),
    url('^abuse/', views.report_abuse, name='addons.abuse'),
    url('^share$', views.share, name='addons.share'),
    url('^developers$', views.developers,
        {'page': 'developers'}, name='addons.meet'),
    url('^contribute/roadblock/', views.developers,
        {'page': 'roadblock'}, name='addons.roadblock'),
    url('^contribute/installed/', views.developers,
        {'page': 'installed'}, name='addons.installed'),
    url('^contribute/thanks',
        csrf_exempt(lambda r, addon_id: redirect('addons.detail', addon_id)),
        name='addons.thanks'),
    url('^contribute/$', views.contribute, name='addons.contribute'),
    url('^contribute/(?P<status>cancel|complete)$', views.paypal_result,
        name='addons.paypal'),


    url('^about$', lambda r, addon_id: redirect('addons.installed',
                                                 addon_id, permanent=True),
                   name='addons.about'),

    ('^reviews/', include('reviews.urls')),
    ('^statistics/', include('stats.urls')),
    ('^versions/', include('versions.urls')),
)


impala_detail_patterns = patterns('',
    url('^$', views.impala_addon_detail, name='addons.i_detail'),
    ('^reviews/', include('reviews.impala_urls')),
    url('^developers$', views.impala_developers, {'page': 'developers'},
        name='addons.i_meet'),
    url('^contribute/roadblock/', views.impala_developers,
        {'page': 'roadblock'}, name='addons.i_roadblock'),
    url('^contribute/installed/', views.impala_developers,
        {'page': 'installed'}, name='addons.i_installed'),
)


urlpatterns = patterns('',
    # The homepage.
    url('^$', views.home, name='home'),
    # The impala homepage.
    url('^i/$', views.impala_home, name='i_home'),
    # Promo modules for the homepage
    url('^i/promos$', views.homepage_promos, name='addons.homepage_promos'),

    # URLs for a single add-on.
    ('^addon/%s/' % ADDON_ID, include(detail_patterns)),
    # Impala deets.
    url('^i/addon/%s/' % ADDON_ID, include(impala_detail_patterns)),

    # Accept extra junk at the end for a cache-busting build id.
    url('^addons/buttons.js(?:/.+)?$', 'addons.buttons.js'),

    # For happy install button debugging.
    url('^addons/smorgasbord$', 'addons.buttons.smorgasbord'),

    # Remora EULA and Privacy policy URLS
    ('^addons/policy/0/(?P<addon_id>\d+)/(?P<file_id>\d+)',
     lambda r, addon_id, file_id: redirect('addons.eula',
                                  addon_id, file_id, permanent=True)),
    ('^addons/policy/0/(?P<addon_id>\d+)/',
     lambda r, addon_id: redirect('addons.privacy',
                                  addon_id, permanent=True)),

    ('^versions/license/(\d+)$', views.license_redirect),
)
