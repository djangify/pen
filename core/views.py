# core/views.py
from django.shortcuts import render
from django.utils import timezone
from blog.models import Post
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse

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


def policies_index(request):
    """
    View for the index of policies page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': None}
    ]
    
    context = {
        'title': 'Index of all Policies for Pen & I Publishing',
        'meta_description': 'This is the most up to date index of all policies for our website.',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/policies_index.html', context)


def privacy_policy(request):
    """
    View for the privacy policy page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': reverse('core:policies_index')},
        {'title': 'Privacy Policy', 'url': None}
    ]
    
    context = {
        'title': 'Privacy Policy for Pen & I Publishing',
        'meta_description': 'This is the most up to date privacy policy for our website',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/privacy_policy.html', context)


def terms_conditions(request):
    """
    View for the terms and conditions policy page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': reverse('core:policies_index')},
        {'title': 'Terms & Conditions', 'url': None}
    ]
    
    context = {
        'title': 'Terms and Conditions Policy for Pen & I Publishing',
        'meta_description': 'This is the most up to date terms and conditions policy for our website',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/terms_conditions.html', context)

def advertising_policy(request):
    """
    View for the advertising policy page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': reverse('core:policies_index')},
        {'title': 'Advertising Policy', 'url': None}
    ]
    
    context = {
        'title': 'Advertising Policy for Pen & I Publishing',
        'meta_description': 'This is the most up to date advertising policy for our website',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/advertising_policy.html', context)

def support_policy(request):
    """
    View for the help and support policy page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': reverse('core:policies_index')},
        {'title': 'Help & Support', 'url': None}
    ]
    
    context = {
        'title': 'Help and Support Policy for Pen & I Publishing',
        'meta_description': 'This is the most up to date help and support policy for our website',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/support_policy.html', context)


def cookies_policy(request):
    """
    View for the cookies policy page
    """
    breadcrumbs = [
        {'title': 'Policies', 'url': reverse('core:policies_index')},
        {'title': 'Cookies Policy', 'url': None}
    ]
    
    context = {
        'title': 'Cookies Policy for Pen & I Publishing',
        'meta_description': 'This is the most up to date cookies policy for our website',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'policy/cookies_policy.html', context)


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

