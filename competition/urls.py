from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('spartakiada.urls')),
    path('', include('loging.urls')),
    path('admin/', admin.site.urls),
]