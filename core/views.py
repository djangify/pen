# core/views.py
from django.shortcuts import render
from django.utils import timezone
from blog.models import Post

def home_view(request):
    # Get the latest 3 published blog posts
    latest_posts = Post.objects.filter(
        status="published", 
        publish_date__lte=timezone.now()
    ).order_by("-publish_date")[:3]
    
    context = {
        'latest_posts': latest_posts,
    }
    
    return render(request, 'index.html', context)

def about(request):
    """
    View for the About page
    """
    context = {
        'title': 'About Pen and I Publishing',
        'meta_description': 'Learn about Pen and I Publishing and our mission to help everyone capture their life stories and memories.',
    }
    return render(request, 'core/about.html', context)

def notebook(request):
    """
    View for the Notebook page
    """
    context = {
        'title': 'Paperback Notebooks by Pen & I Publishing',
        'meta_description': 'We create lined paperback notebooks to help you capture your life stories and memories.',
    }
    return render(request, 'core/paperback_notebook.html', context)