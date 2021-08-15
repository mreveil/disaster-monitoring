# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
import app.views as aviews

router = routers.DefaultRouter()
router.register(r"users", aviews.UserViewSet)
router.register(r"groups", aviews.GroupViewSet)
router.register(r"reports", aviews.ReportViewSet)
router.register(r"authors", aviews.AuthorViewSet)


urlpatterns = [
    # path('chart/<str:symbol_name>/', views.chart, name='chart'),
    # path('livedata/', views.add_data, name='livedata'),
    # # path('chat/', views.index, name='index'),
    # path('chat/<str:room_name>/', views.room, name='room'),
    path("api-token-auth/", views.obtain_auth_token),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),  # Django admin route
    path("", include("authentication.urls")),  # Auth routes - login / register
    path("", include("app.urls")),  # UI Kits Html files
]
