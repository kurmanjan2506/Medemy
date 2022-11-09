"""EducateApi URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from EducateApi import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
# from buy_course.views import UsersCourseViewSet
from course.views import CourseViewSet, CategoryViewSet, WhatYouLearnViewSet, RequirementsViewSet, LessonViewSet, \
    VideoViewSet, LevelViewSet
from rap.views import auth
from rating.views import ReviewViewSet
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


# Для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Education_platform test project",
      default_version='v1',
      description="Test REST API backend at django",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Роутеры для вьюшек
router = SimpleRouter()
router.register('courses', CourseViewSet)
router.register('categories', CategoryViewSet)
router.register('level', LevelViewSet)
router.register('reviews', ReviewViewSet)
router.register('course/what_learn', WhatYouLearnViewSet)
router.register('course/requirements', RequirementsViewSet)
router.register('course/lesson', LessonViewSet)
router.register('course/lesson/video', VideoViewSet)
# router.register('buy_course', UsersCourseViewSet)


# Основные urls
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('', include('social_django.urls', namespace='social')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('rap.urls')),
    path('api/v1/', include(router.urls)),
    path('auth/', auth),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/', include('buy_course.urls')),
    path('', include('video_chat.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('chat/', include('chat.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
