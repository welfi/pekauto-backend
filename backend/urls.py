from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_vin, name='add_vin'),
    path('search/', views.search_vin, name='search_vin'),
    path('browse/', views.list_all_vins, name='list_all'),
    path('total_pages/', views.get_total_pages, name='total_pages')
]
