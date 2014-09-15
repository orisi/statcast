from django.conf.urls import patterns, url, include
from rest_framework import routers, permissions
from monitor import views

import django_cron
django_cron.autodiscover()


#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

#router.register(r'messages', views.MsgViewSet)

from rest_framework.urlpatterns import format_suffix_patterns

import settings
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.

urlpatterns = patterns('',

        # unhash this to get access to json user/group api
        #url(r'^meta/', include(router.urls)),
        url(r'^storage/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),

        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        )


urlpatterns_to_suffix = patterns('',

        url(r'^log/(?P<pk>[0-9]+)/$', views.MonitorDetail.as_view()),
        url(r'^logs/', views.MonitorList.as_view()),
        url(r'^last/', views.MonitorListLast.as_view()),

         url(r'^$', views.MonitorList.as_view()),
       
        )
 
 
urlpatterns_suffixed = format_suffix_patterns(urlpatterns_to_suffix)

urlpatterns += urlpatterns_suffixed


