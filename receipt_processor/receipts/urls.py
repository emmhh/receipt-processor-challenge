from django.urls import path
from . import views

urlpatterns = [
    path('receipts/process', views.process_receipt, name='process_receipt'),
    path('receipts/<str:id>/points', views.get_points, name='get_points'),
]