# prompt/views.py

from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Tag, PromptCategory, WritingPrompt
from .serializers import TagSerializer, PromptCategorySerializer, WritingPromptSerializer
import random

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class PromptCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromptCategory.objects.all()
    serializer_class = PromptCategorySerializer
    permission_classes = [permissions.AllowAny]

class WritingPromptViewSet(viewsets.ReadOnlyModelViewSet):  # Changed to ReadOnlyModelViewSet
    queryset = WritingPrompt.objects.filter(active=True)
    serializer_class = WritingPromptSerializer
    permission_classes = [permissions.AllowAny]  # Changed to AllowAny
    
    def get_queryset(self):
        """
        Allow filtering by query parameters
        """
        queryset = WritingPrompt.objects.filter(active=True)
        
        # Get query parameters
        category_slug = self.request.query_params.get('category__slug', None)
        difficulty = self.request.query_params.get('difficulty', None)
        prompt_type = self.request.query_params.get('prompt_type__in', None)
        
        # Apply filters if provided
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        if prompt_type:
            prompt_types = prompt_type.split(',')
            queryset = queryset.filter(prompt_type__in=prompt_types)
            
        return queryset

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def random_prompt(request):
    """
    Get a random writing prompt with optional filters
    """
    # Get filter parameters
    category_slug = request.query_params.get('category', None)
    difficulty = request.query_params.get('difficulty', None)
    prompt_type = request.query_params.get('type', None)
    
    # Start with all active prompts
    prompts = WritingPrompt.objects.filter(active=True)
    
    # Apply filters if provided
    if category_slug:
        prompts = prompts.filter(category__slug=category_slug)
    
    if difficulty:
        prompts = prompts.filter(difficulty=difficulty)
    
    if prompt_type:
        if prompt_type != 'both':
            prompts = prompts.filter(prompt_type__in=[prompt_type, 'both'])
    
    # Check if we have any prompts after filtering
    if not prompts.exists():
        return Response({"error": "No prompts found with the given criteria"}, status=404)
    
    # Select a random prompt
    prompt = random.choice(prompts)
    serializer = WritingPromptSerializer(prompt)
    
    return Response(serializer.data)
