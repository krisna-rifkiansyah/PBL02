from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.car_list, name='car_list'),
    path('create/', views.car_create, name='car_create'),
    path('update/<int:id>/', views.car_update, name='car_update'),
    path('delete/<int:id>/', views.car_delete, name='car_delete'),
    path('import/', views.import_csv, name='import_csv'),
]
