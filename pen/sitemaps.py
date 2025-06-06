from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post, Category
from prompt.models import PromptCategory

class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['core:home', 'core:about', 'core:notebook', 
                'core:privacy_policy', 'core:advertising_policy', 
                'core:terms_conditions', 'blog:list', 
                'accounts:login', 'accounts:register']

    def location(self, item):
        url = reverse(item)
        # Django's reverse shouldn't include protocol, but just to be safe
        if '://' in url:
            url = url.split('://', 1)[1]
        return url


class BlogPostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated

class BlogCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

class PromptCategorySitemap(Sitemap):
    changefreq = "monthly" 
    priority = 0.7

    def items(self):
        return PromptCategory.objects.all()
    