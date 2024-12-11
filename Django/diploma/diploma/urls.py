"""
URL configuration for diploma project.

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
from django.urls import path
from my_project.views import sign_up, base, main, log_out, lenta, add_recipe, add_favorites, selected, remove_favorites
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', sign_up),
    path('', main),
    path('main/', main),
    path('logout', log_out),
    path('lenta/', lenta),
    path('add_recipe/', add_recipe),
    path('add_favorites/<int:recipe_id>/', add_favorites, name='add_favorites'),
    path('selected', selected),
    path('remove_favorites/<int:recipe_id>/', remove_favorites, name='remove_favorites')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
