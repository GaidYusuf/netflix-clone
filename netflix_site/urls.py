"""
URL configuration for netflix_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin  #  Admin interface to allow manage application's data through a web interface
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # This function is used to serve static (e.g., CSS, JavaScript) and media files (e.g., images) during development

# Define the list of URL patterns that route URLs to views
urlpatterns = [
    path('admin/', admin.site.urls),  # Route for the admin interface. Access this at '/admin/' URL
    path('', include('core.urls'))  # Include the URL configurations from the 'core' app
]

# Append URL patterns to serve media files during development
# static() is used to serve media files. settings.MEDIA_URL is the base URL for media files.
# settings.MEDIA_ROOT is the filesystem path where media files are stored.

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)