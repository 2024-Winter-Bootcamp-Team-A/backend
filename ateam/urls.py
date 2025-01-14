"""
URL configuration for ateam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title="BookShorts",
        default_version='1.0',
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('api/v1/books/', include('books.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/shorts/', include('shorts.urls')),
    path('api/v1/shorts/', include('wishes.urls')),
    path('api/v1/shorts/', include('records.urls')),
    path('api/v1/shorts/', include('comments.urls')),
    path('api/v1/stats/', include('stats.urls')),
    path('api/v1/todays-shorts/', include('todays_shorts.urls')),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
