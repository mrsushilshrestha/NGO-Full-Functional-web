from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    """Program category"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    """Program/Event model"""
    CATEGORY_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('past', 'Past'),
    ]
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    description = RichTextField()
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    event_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='upcoming')
    category_tag = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title
