from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticSitemap,
    BlogPostSitemap,
    BlogCategorySitemap,
    PromptCategorySitemap,
)

sitemaps = {
    "static": StaticSitemap,
    "blog": BlogPostSitemap,
    "categories": BlogCategorySitemap,
    "prompt_categories": PromptCategorySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("prompt/", include("prompt.urls")),
    path("blog/", include("blog.urls", namespace="blog")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "media/<path:path>",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
]
