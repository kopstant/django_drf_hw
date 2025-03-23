from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lms.urls', namespace='lms')),
    path('users/', include('users.urls', namespace='users')),
]
