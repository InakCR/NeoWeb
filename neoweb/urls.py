from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('linguista.urls')),
    path('linguista/', include('linguista.urls')),
    path('admin/', admin.site.urls),
]