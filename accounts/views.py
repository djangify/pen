# accounts/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from prompt.models import WritingPrompt
from .forms import UserRegistrationForm, UserProfileForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Pen and I Publishing.')
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            # Redirect to the page the user was trying to access, or home
            next_page = request.GET.get('next', 'core:home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    favourite_prompts = request.user.profile.favourite_prompts.all()
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'favourite_prompts': favourite_prompts
    })

@login_required
def add_favourite_prompt(request, prompt_id):
    prompt = get_object_or_404(WritingPrompt, id=prompt_id)
    user_profile = request.user.profile
    
    if prompt in user_profile.favourite_prompts.all():
        user_profile.favourite_prompts.remove(prompt)
        messages.success(request, 'Prompt removed from your favourites.')
    else:
        user_profile.favourite_prompts.add(prompt)
        messages.success(request, 'Prompt added to your favourites.')
    
    # If the request is AJAX, return a JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_favourite': prompt in user_profile.favourite_prompts.all()
        })
    
    # Otherwise redirect back to referring page
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))