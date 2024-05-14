from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_diseases, name='index'),
    path('crawl/', views.crawl, name='crawl'),
    path('register/', views.register_doctor, name='register_doctor'),
    path('login/', views.doctor_login, name='doctor_login'),
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('logout/', views.doctor_logout, name='logout'),
    path('add_doctor_info/', views.add_doctor_info, name='add_doctor_info'),
]
