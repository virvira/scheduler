"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from todolist import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('oauth/', include('social_django.urls', namespace='social'))

]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]

# from django.urls import include, path
# from rest_framework.routers import SimpleRouter
# from rest_framework_nested.routers import NestedSimpleRouter
#
# from ads.views import AdViewSet, CommentViewSet
#
# ads_router = SimpleRouter()
# ads_router.register('ads', AdViewSet, basename='ads')
# comments_router = NestedSimpleRouter(ads_router, 'ads', lookup='ad')
# comments_router.register('comments', CommentViewSet, basename='comments')
#
# urlpatterns = [
#     path('', include(ads_router.urls)),
#     path('', include(comments_router.urls))
# ]
