from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [

    path('', lambda request: HttpResponse("Backend is running"), name='home'),

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]