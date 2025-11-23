
from django.urls import path
from . import views

urlpatterns = [
    path('equipment/', views.upload_equipment_data, name='upload_equipment_data'),
    path('history/', views.get_upload_history, name='get_upload_history'),
]