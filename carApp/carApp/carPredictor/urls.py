from django.urls import path
from . import views

urlpatterns = [
    path('welcome', views.welcome),
    path('carApp', views.carApp),
    path('oil_car', views.oil_car),
    path('load_models/<int:car_make_id>/', views.load_models, name='load_models'),
    path('load_versions/<int:car_model_id>/', views.load_versions, name='load_versions')
]