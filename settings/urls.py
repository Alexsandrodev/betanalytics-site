from django.contrib import admin
from django.urls import path, include # adicionar include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views
import myapp.urls


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('accounts.urls')),
    path('', include(myapp.urls)),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 