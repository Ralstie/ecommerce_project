from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('store.urls')
    ),

    path(
        'api/',
        include('store.api_urls')
    ),

    path(
        'api-token-auth/',
        auth_views.obtain_auth_token,
        name='api_token_auth'
    ),

    path(
        'api-auth/',
        include('rest_framework.urls')
    ),
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )