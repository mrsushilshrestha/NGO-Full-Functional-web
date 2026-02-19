from django.db import models
from ckeditor.fields import RichTextField


class OrganizationInfo(models.Model):
    """Organization mission, vision, objectives"""
    mission = RichTextField(blank=True)
    vision = RichTextField(blank=True)
    objectives = RichTextField(blank=True)
    history = RichTextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Organization Info'

    def __str__(self):
        return 'Organization Info'


class Founder(models.Model):
    """Founder details"""
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='founders/', blank=True, null=True)
    bio = RichTextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class ChapterLocation(models.Model):
    """Chapter/location details"""
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    map_embed = models.TextField(blank=True, help_text='Google Maps embed code')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class Achievement(models.Model):
    """Key achievements"""
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True)
    year = models.CharField(max_length=20, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
