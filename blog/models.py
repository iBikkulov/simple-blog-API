from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    content = models.TextField()
    excerpt = models.TextField(null=True)
    published = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    status = models.CharField(max_length=10, choices=options,
        default='published')
    title = models.CharField(max_length=250)

    objects = models.Manager()
    postobjects = PostManager() # Only published posts

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title