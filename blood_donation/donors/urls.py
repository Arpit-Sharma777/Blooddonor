from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_donor, name='register_donor'),
    path('donors/', views.donor_list, name='donor_list'),
    path('blood_banks/', views.blood_bank_list, name='blood_bank_list'),
    path('blood_bank_dashboard/', views.blood_bank_dashboard, name='blood_bank_dashboard'),
    path('add_blood_bank/', views.add_blood_bank, name='add_blood_bank'),
    path('blood_bank_update/<int:pk>/', views.blood_bank_update, name='blood_bank_update'),
    path('blood_bank_delete/<int:pk>/', views.blood_bank_delete, name='blood_bank_delete'),

]
