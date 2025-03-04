from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Category
from django.utils import timezone


def blog_list(request):
    posts = Post.objects.filter(
        status="published", publish_date__lte=timezone.now()
    ).select_related("category")

    paginator = Paginator(posts, 12)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    context = {
        "posts": posts,
        "categories": Category.objects.all(),
        "title": "Blog",
        "meta_description": "Posts and updates from Pen And I Publishing",
        
    }

    return render(request, "blog/list.html", context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category, status="published", publish_date__lte=timezone.now()
    ).order_by(
        "-publish_date"
    )  

    paginator = Paginator(posts, 12)
    page = request.GET.get("page")
    posts = paginator.get_page(page)

    context = {
        "category": category,
        "posts": posts,
        "categories": Category.objects.all(),
        "title": f"{category.name} - Blog",
        "meta_description": f"Latest about {category.name} from Pen And I Publishing",
    }

    return render(request, "blog/category.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post, slug=slug, status="published", publish_date__lte=timezone.now()
    )

    # Get next and previous posts
    next_post = (
        Post.objects.filter(
            status="published",
            publish_date__lte=timezone.now(),
            publish_date__gt=post.publish_date,
        )
        .order_by("publish_date")
        .first()
    )

    previous_post = (
        Post.objects.filter(
            status="published",
            publish_date__lte=timezone.now(),
            publish_date__lt=post.publish_date,
        )
        .order_by("-publish_date")
        .first()
    )

    # Get related posts from same category
    related_posts = (
        Post.objects.filter(
            status="published", publish_date__lte=timezone.now(), category=post.category
        )
        .exclude(id=post.id)
        .select_related("category")[:2]
    )

    context = {
        "post": post,
        "next_post": next_post,
        "previous_post": previous_post,
        "related_posts": related_posts,
        "categories": Category.objects.all(),
        "title": post.meta_title or post.title,
        "meta_description": post.meta_description,
        "meta_keywords": post.meta_keywords,
        "user": request.user,
    }
    return render(request, "blog/detail.html", context)
