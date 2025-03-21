from django.urls import path 
from myapp import views

urlpatterns = [
    path('', views.base, name='home'),
    path('betano/inicio/', views.betano, name="betano"),
    path('betano/horarios/', views.horarios_betano, name='horarios_betano'),
    path('betano/horarios/tabela', views.tabela, name='tabela')
]