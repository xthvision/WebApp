
from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), #also the login page
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('result/', include('results.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
