"""Blog models for editorial content with structured sections."""
from django.db import models
from django.urls import reverse


class BlogAuthor(models.Model):
    """Author for blog posts."""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True, help_text='e.g. Health Officer, Field Coordinator')
    avatar = models.ImageField(upload_to='blog/authors/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    """Category for blog posts."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Blog categories'

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    """Tag for blog posts - topics."""
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, max_length=80)
    order = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False, help_text='Show in popular tags filter')

    class Meta:
        ordering = ['-is_popular', 'order', 'name']

    def __str__(self):
        return self.name



class BlogPost(models.Model):
    """Blog post with rich content blocks."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    slug = models.SlugField(unique=True, max_length=300)
    title = models.CharField(max_length=400)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Author - can use linked author or inline fields
    author = models.ForeignKey(
        BlogAuthor, on_delete=models.SET_NULL, null=True, blank=True,
        help_text='Leave blank to use author name/role/avatar below'
    )
    author_name = models.CharField(max_length=200, blank=True)
    author_role = models.CharField(max_length=200, blank=True)
    author_avatar = models.ImageField(upload_to='blog/authors/', blank=True, null=True)

    category = models.ForeignKey(
        BlogCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(BlogTag, blank=True)

    excerpt = models.TextField(
        max_length=300,
        help_text='Short excerpt for listing cards'
    )
    long_excerpt = models.TextField(
        blank=True,
        help_text='Long intro paragraph for detail page'
    )

    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    image_caption = models.CharField(max_length=400, blank=True)

    featured = models.BooleanField(
        default=False,
        help_text='Show as featured post on listing'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_author_display(self):
        if self.author:
            return self.author.name
        return self.author_name or 'NHAF Nepal'

    def get_author_role(self):
        if self.author:
            return self.author.role
        return self.author_role or ''

    def get_author_avatar(self):
        if self.author and self.author.avatar:
            return self.author.avatar
        return self.author_avatar


class BlogContentBlock(models.Model):
    """Modular content section for blog posts."""
    TYPE_CHOICES = [
        ('paragraph', 'Paragraph'),
        ('heading', 'Heading'),
        ('quote', 'Quote'),
        ('list', 'Bulleted List'),
    ]
    post = models.ForeignKey(
        BlogPost, on_delete=models.CASCADE, related_name='content_blocks'
    )
    block_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    content = models.TextField(blank=True)
    attribution = models.CharField(
        max_length=300, blank=True,
        help_text='For quotes: attribution line'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.get_block_type_display()} (order {self.order})'

    def get_list_items(self):
        """Parse content as newline-separated list items."""
        if not self.content:
            return []
        return [line.strip() for line in self.content.strip().split('\n') if line.strip()]


class BlogPageSettings(models.Model):
    """CMS-editable settings for blog listing page."""
    hero_title = models.CharField(
        max_length=200,
        default='Blog',
        help_text='Page title (e.g. Blog, Stories from the Field)'
    )
    hero_subtitle = models.TextField(
        blank=True,
        default='Read about our health outreach, community programs, and impact across Nepal.',
        help_text='Subtitle / description below title'
    )
    banner_image = models.ImageField(
        upload_to='blog/banner/',
        blank=True,
        null=True,
        help_text='Optional hero banner image (uses default if empty)'
    )
    posts_per_page = models.PositiveIntegerField(
        default=9,
        help_text='Number of posts per page'
    )
    enable_featured_layout = models.BooleanField(
        default=False,
        help_text='Show one post as large featured card above the grid'
    )
    SORT_CHOICES = [
        ('latest', 'Latest first'),
        ('oldest', 'Oldest first'),
    ]
    default_sort = models.CharField(
        max_length=20,
        choices=SORT_CHOICES,
        default='latest'
    )
    seo_title = models.CharField(
        max_length=200,
        blank=True,
        help_text='SEO meta title for blog listing page'
    )
    seo_description = models.TextField(
        blank=True,
        max_length=320,
        help_text='SEO meta description for blog listing page'
    )
    enable_swipe_effect = models.BooleanField(
        default=True,
        help_text='Swipe/slide card image to reveal title'
    )
    enable_auto_search = models.BooleanField(
        default=True,
        help_text='Show real-time search suggestions'
    )
    # Page title controls
    show_title = models.BooleanField(
        default=True,
        help_text='Show or hide the main blog page title'
    )
    # Post appearance
    post_title_color = models.CharField(
        max_length=20, blank=True, default='#111827',
        help_text='CSS color for post titles'
    )
    post_content_color = models.CharField(
        max_length=20, blank=True, default='#4b5563',
        help_text='CSS color for post content/body'
    )
    post_title_font_size_px = models.PositiveIntegerField(
        default=20,
        help_text='Title font size in pixels'
    )
    post_body_font_size_px = models.PositiveIntegerField(
        default=15,
        help_text='Body font size in pixels'
    )
    post_title_font_family = models.CharField(
        max_length=100, blank=True,
        default="'Playfair Display', Georgia, serif",
        help_text='CSS font-family for titles'
    )
    post_body_font_family = models.CharField(
        max_length=100, blank=True,
        default="'Inter', system-ui, sans-serif",
        help_text='CSS font-family for body text'
    )
    card_bg_color = models.CharField(
        max_length=20, blank=True, default='#fdfdfd',
        help_text='Background color for blog cards'
    )
    card_border_color = models.CharField(
        max_length=20, blank=True, default='rgba(0,0,0,0.06)',
        help_text='Border color for blog cards'
    )
    CARD_SHADOW_CHOICES = [
        ('none', 'None'),
        ('light', 'Light'),
        ('medium', 'Medium'),
    ]
    card_shadow_style = models.CharField(
        max_length=10, choices=CARD_SHADOW_CHOICES,
        default='light',
        help_text='Shadow intensity for blog cards'
    )
    # Global style controls (blog-specific)
    primary_color = models.CharField(
        max_length=20, blank=True, default='#0B5345',
        help_text='Primary theme color for blog'
    )
    secondary_color = models.CharField(
        max_length=20, blank=True, default='#148f77',
        help_text='Secondary theme color for blog'
    )
    link_color = models.CharField(
        max_length=20, blank=True, default='#0B5345',
        help_text='Default link color in blog content'
    )
    button_color = models.CharField(
        max_length=20, blank=True, default='#0B5345',
        help_text='Primary button color in blog'
    )
    global_card_bg_color = models.CharField(
        max_length=20, blank=True, default='#f9fafb',
        help_text='Background color for generic blog panels'
    )
    TEXT_ALIGN_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('justify', 'Justify'),
    ]
    text_align = models.CharField(
        max_length=10, choices=TEXT_ALIGN_CHOICES,
        default='left',
        help_text='Default text alignment for blog paragraphs'
    )

    class Meta:
        verbose_name = 'Blog page settings'
        verbose_name_plural = 'Blog page settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
