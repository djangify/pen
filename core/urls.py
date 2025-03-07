# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),
    path('paperback_notebook', views.notebook, name='notebook' ),
    path('policy/privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('policy/advertising-policy/', views.advertising_policy, name='advertising_policy'),
    path('policy/terms-conditions/', views.terms_conditions, name='terms_conditions')
]