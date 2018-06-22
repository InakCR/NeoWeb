from django.urls import path

from . import views

app_name = 'linguista'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalogar/', views.catalogar, name='catalogar'),
    path('admitir/', views.admitir, name='admitir'),
    path('denegar/', views.denegar, name='denegar'),
    path('procesar/', views.procesar, name='procesar'),
    path('proceso/', views.proceso, name='proceso'),
    path('l/', views.index_by, name='index_by'),
    path('n/', views.index_by_neo, name='index_by_neo'),
    path('buscar/', views.buscar, name='buscar'),
    path('login/', views.loguearse, name='loguearse'),
]
