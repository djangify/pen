# prompt/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'prompt'

router = DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'categories', views.PromptCategoryViewSet)
router.register(r'prompts', views.WritingPromptViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/random-prompt/', views.random_prompt, name='random-prompt'),
]