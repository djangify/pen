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
    queryset = PromptCategory.objects.all().order_by('name')
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
# prompt/views.py (partial - only the random_prompt function)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def random_prompt(request):
    """
    Get a random writing prompt with optional filters,
    tracking previously shown prompts via session to avoid repetition.
    """
    # Get filter parameters
    category_slug = request.query_params.get('category', None)
    difficulty = request.query_params.get('difficulty', None)
    prompt_type = request.query_params.get('type', None)
    
    # Get current prompt ID to exclude (for "Get Another Prompt")
    current_prompt_id = request.query_params.get('current_id', None)
    
    # Start with all active prompts
    prompts = WritingPrompt.objects.filter(active=True)
    
    # Log filtering parameters for debugging
    print(f"Filtering prompts with: category={category_slug}, difficulty={difficulty}, type={prompt_type}, current_id={current_prompt_id}")
    print(f"Initial prompt count: {prompts.count()}")
    
    # Apply filters if provided
    if category_slug and category_slug != '':
        prompts = prompts.filter(category__slug=category_slug)
        print(f"After category filter: {prompts.count()} prompts")
    
    if difficulty and difficulty != '':
        prompts = prompts.filter(difficulty=difficulty)
        print(f"After difficulty filter: {prompts.count()} prompts")
    
    if prompt_type and prompt_type != '' and prompt_type != 'both':
        prompts = prompts.filter(prompt_type__in=[prompt_type, 'both'])
        print(f"After type filter: {prompts.count()} prompts")
    
    # Exclude current prompt if getting another one
    if current_prompt_id and current_prompt_id.isdigit():
        prompts = prompts.exclude(id=int(current_prompt_id))
        print(f"After excluding current prompt: {prompts.count()} prompts")
    
    # Initialize the session if it doesn't exist
    if not request.session.session_key:
        request.session.save()
    
    # Get shown prompts from session
    session_key = f"shown_prompts_{category_slug or 'all'}_{difficulty or 'all'}_{prompt_type or 'all'}"
    shown_prompts = request.session.get(session_key, [])
    
    print(f"Previously shown prompts for this session/filter combination: {shown_prompts}")
    
    # Create a working copy of the queryset before applying session-based filtering
    available_prompts = prompts
    
    # If we have shown prompts and there are enough prompts to filter
    # Only exclude previously shown prompts if we still have plenty to show
    if shown_prompts and available_prompts.count() > len(shown_prompts) / 2:
        # Create a list of IDs to exclude
        prompts_to_exclude = [id for id in shown_prompts if isinstance(id, int)]
        
        # Apply the exclusion filter
        available_prompts = available_prompts.exclude(id__in=prompts_to_exclude)
        print(f"After excluding previously shown prompts: {available_prompts.count()} prompts")
    
    # Check if we have any prompts after all filtering
    if not available_prompts.exists():
        # If we've excluded all prompts based on session history, reset and use all prompts
        if prompts.exists():
            print("All matching prompts have been shown already, resetting history")
            available_prompts = prompts
            shown_prompts = []  # Reset the shown prompts
            request.session[session_key] = shown_prompts
        else:
            # If there are no prompts with the current filters
            if current_prompt_id:
                # If we're trying to get another prompt but none are available
                response_data = {
                    "message": "You've seen all prompts matching these filters. Try different options.",
                    "no_more_prompts": True
                }
                print("No more prompts available with these filters")
                return Response(response_data, status=200)
            else:
                # No prompts at all with these filters
                response_data = {
                    "message": "No prompts found with these filters. Try different options.",
                    "no_prompts": True
                }
                print("No prompts available with these filters")
                return Response(response_data, status=200)
    
    # Select a random prompt
    prompt = random.choice(list(available_prompts))
    
    # Add to shown prompts
    if prompt.id not in shown_prompts:
        shown_prompts.append(prompt.id)
        # Limit to last 30 to avoid session bloat
        if len(shown_prompts) > 30:
            shown_prompts = shown_prompts[-30:]
        request.session[session_key] = shown_prompts
        # Save session explicitly to ensure it's stored
        request.session.modified = True
    
    print(f"Selected prompt ID: {prompt.id}, updated shown_prompts: {shown_prompts}")
    
    # Serialize and return the selected prompt
    serializer = WritingPromptSerializer(prompt)
    response_data = serializer.data
    
    # Add a flag indicating this is a valid prompt response
    response_data['is_valid_prompt'] = True
    
    return Response(response_data)
