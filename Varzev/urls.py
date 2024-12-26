"""
URL configuration for Varzev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# made by AmirTheEngineer 
# https://t.me/AmirOmidi.Dev

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Varzev import settings
from Varzev.settings import MEDIA_ROOT

urlpatterns = [
    path('varzev-admin-control-panel/', admin.site.urls),
    path('accounts/', include('account.urls'), name='account'),
    path('', include('complex.urls'), name='home'),
    path('captcha/', include('captcha.urls'), name='captcha'),
    path('reserve/', include('payment.urls'), name='payments'),
]+static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
