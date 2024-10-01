from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

User = get_user_model()

class Blog(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    summary = RichTextField(blank=True)
    content = RichTextField()  # Rich text for content
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100, blank=True, null=True)  # Allow anonymous names
    author_email = models.EmailField(blank=True, null=True)  # Allow anonymous emails
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_name or 'Anonymous'}"
