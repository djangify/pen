from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from tinymce.models import HTMLField 


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    AD_TYPE_CHOICES = [
        ("none", "No Advertisement"),
        ("adsense", "Google AdSense"),
        ("banner", "Banner Image"),
    ]
    RESOURCE_TYPES = [
        ("none", "No Resource"),
        ("pdf", "PDF Document"),
    ]

    # Basic fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # Dates
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    # Content
    content = HTMLField(verbose_name="Blog Content")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default="none")
    resource_title = models.CharField(max_length=100, blank=True, help_text="Title for the downloadable resource")
    resource = models.FileField(upload_to="blog/resources/", null=True, blank=True)

    # Media fields
    image = models.ImageField(
        upload_to="blog/images/", null=True, blank=True
    )
    external_image_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="External URL for product image (jpg/png only)",
    )
    youtube_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="blog/thumbnails/", null=True, blank=True
    )
    thumbnail = models.ImageField(
        upload_to="blog/thumbnails/", null=True, blank=True
    )
    @property
    def get_meta_title(self):
        """Get meta title with fallback logic"""
        return self.meta_title or self.title[:60]
    
    @property
    def get_meta_description(self):
        """Get meta description with fallback logic"""
        if self.meta_description:
            return self.meta_description
        
        # If you have an introduction/excerpt field
        if hasattr(self, 'introduction') and self.introduction:
            from django.utils.html import strip_tags
            clean_intro = strip_tags(self.introduction)
            return clean_intro[:160]
        
        # Fall back to content
        if self.content:
            from django.utils.html import strip_tags
            clean_content = strip_tags(self.content)
            return clean_content[:160]
        
        # Last resort: use title
        return f"{self.title} - {self.category.name if hasattr(self, 'category') else ''}"[:160]


    def get_image_url(self):
        """Get the URL for the main image"""
        try:
            if self.external_image_url:
                return self.external_image_url
            if self.image:
                return self.image.url
            return None
        except Exception:
            return None

    def get_ad_image_url(self):
        """Get the URL for the advertisement image"""
        try:
            if self.ad_image:
                return self.ad_image.url
            return None
        except Exception:
            return None
    

    def get_thumbnail_url(self):
        """Get the thumbnail URL - falls back to main image if no thumbnail"""
        try:
            return self.thumbnail.url if self.thumbnail else self.get_image_url()
        except Exception:
            return None

    # Advertisement fields
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES, default="none")
    ad_code = models.TextField(blank=True)
    ad_image = models.ImageField(
        upload_to="ads/", null=True, blank=True, 
    )
    ad_url = models.URLField(blank=True)

    # SEO fields
    meta_title = models.CharField(
        max_length=60, blank=True, help_text="SEO Title (60 characters max)"
    )
    meta_description = models.CharField(
        max_length=160, blank=True, help_text="SEO Description (160 characters max)"
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated keywords"
    )

    class Meta:
        ordering = ["-publish_date", "-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-set publish date when status changes to published
        if self.status == "published" and not self.publish_date:
            self.publish_date = timezone.now()

        super().save(*args, **kwargs)

    def get_display_image(self):
        """Get image URL from either uploaded image, thumbnail, or YouTube video"""
        if self.image:
            return self.image.build_url()
        elif self.thumbnail:
            return self.thumbnail.build_url()
        elif self.youtube_url:
            # Extract video ID and return YouTube thumbnail
            if "youtu.be" in self.youtube_url:
                video_id = self.youtube_url.split("/")[-1]
            elif "v=" in self.youtube_url:
                video_id = self.youtube_url.split("v=")[1].split("&")[0]
            else:
                return None
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None

    def get_thumbnail_url(self):
        """Get the thumbnail URL - falls back to main image if no thumbnail"""
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def get_youtube_video_id(self):
        """Extract YouTube video ID from URL"""
        if not self.youtube_url:
            return None

        if "youtu.be" in self.youtube_url:
            return self.youtube_url.split("/")[-1]
        elif "v=" in self.youtube_url:
            return self.youtube_url.split("v=")[1].split("&")[0]

        return None

    def get_youtube_thumbnail(self):
        """Get YouTube video thumbnail URL"""
        if self.youtube_url:
            # Extract video ID from different possible YouTube URL formats
            if "youtu.be" in self.youtube_url:
                video_id = self.youtube_url.split("/")[-1]
            elif "v=" in self.youtube_url:
                video_id = self.youtube_url.split("v=")[1].split("&")[0]
            else:
                return None
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return None

    def get_youtube_embed_url(self):
        """Get YouTube video embed URL"""
        if self.youtube_url:
            if "youtu.be" in self.youtube_url:
                video_id = self.youtube_url.split("/")[-1]
            elif "v=" in self.youtube_url:
                video_id = self.youtube_url.split("v=")[1].split("&")[0]
            else:
                return None
            return f"https://www.youtube.com/embed/{video_id}"
        return None
