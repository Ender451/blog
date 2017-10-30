"""gzystation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^articlelist/', include('article.urls',namespace='articlelist')),                          #文章列表
    url(r'^article/', include('article.urls',namespace='article')),                                  #一般文章
    url(r'^independentarticle/', include('independentarticle.urls',namespace='independentarticle')), #独立文章
    url(r'^online/', include('online.urls', namespace='online')),
    url(r'^search/', include('haystack.urls')),
    url(r'^user/',include('users.urls')),                                                            #用户注册激活
    url(r'', include('home.urls',namespace='home')),
    url(r'', include('comments.urls',namespace='comments')),
    

]
