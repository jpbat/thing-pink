"""thing_pink URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from accounts.urls import urlpatterns as accounts_urls
from feed.urls import urlpatterns as feed_urls

from .views import AppInfo

api_urls = (
    accounts_urls + feed_urls
)

urlpatterns = [
    url(r'^api/v1/status/$', AppInfo.as_view(), name='app-info'),
    url(r'^api/v1/', include(api_urls, namespace='v1'),),
    url(r'^admin/', admin.site.urls),
]
