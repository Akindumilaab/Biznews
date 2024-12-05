"""
URL configuration for Biznews project.

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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from Biznews.userApp.views import SignUpView
from Biznews.blogApp.views import allpostView
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', allpostView, name= 'home' ),
    path('contact/', TemplateView.as_view(template_name = 'contact.html'), name= 'contact' ),
    path('category/', TemplateView.as_view(template_name = 'category.html'), name= 'category' ),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name='signup'),
    re_path(r'^userApp/', include('Biznews.userApp.urls')),
    re_path(r'^userApp/', include('Biznews.blogApp.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



