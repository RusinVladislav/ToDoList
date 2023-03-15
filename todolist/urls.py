from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('core/', include(('todolist.core.urls', 'core'))),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]
