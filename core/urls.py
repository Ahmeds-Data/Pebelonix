# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Ahmed Salim
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),          
    path("", include("apps.authentication.urls")),
    path("", include("apps.home.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
