# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    # add other paths for privacy policy, about page, etc.
    # path('policy/privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('about/', views.about, name='about'),
    path('paperback_notebook', views.notebook, name='notebook' )
]