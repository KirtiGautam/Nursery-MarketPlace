from django.urls import path
from plants import views

app_name = 'plants'

urlpatterns = [
    path('plants/', views.plants, name='plants'),
    path('plant/<int:id>/', views.plantDetails, name='plants'),
    path('orders/', views.orders, name='orders'),
]
