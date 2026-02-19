from django.db import models


class HeroBanner(models.Model):
    """Hero banner for homepage - CMS editable display options"""
    ASPECT_RATIO_CHOICES = [
        ('16:9', '16:9 (Widescreen)'),
        ('21:9', '21:9 (Ultrawide)'),
        ('4:3', '4:3 (Standard)'),
        ('1:1', '1:1 (Square)'),
    ]
    IMAGE_FIT_CHOICES = [
        ('cover', 'Cover (Fill)'),
        ('contain', 'Contain (Fit)'),
    ]
    TEXT_POSITION_CHOICES = [
        ('center', 'Center'),
        ('left', 'Left'),
        ('right', 'Right'),
    ]
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    link_url = models.URLField(blank=True)
    link_text = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    # Display options - editable from CMS
    aspect_ratio = models.CharField(max_length=10, choices=ASPECT_RATIO_CHOICES, default='16:9')
    overlay_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.70,
        help_text='0=transparent, 1=solid. Dark overlay on image for text readability.')
    show_overlay = models.BooleanField(default=True, help_text='Show dark overlay on image')
    image_fit = models.CharField(max_length=10, choices=IMAGE_FIT_CHOICES, default='cover')
    text_position = models.CharField(max_length=10, choices=TEXT_POSITION_CHOICES, default='center')

    def aspect_ratio_css(self):
        """Return aspect ratio for CSS (e.g. 16:9 -> 16/9)"""
        return self.aspect_ratio.replace(':', '/')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class HomeContent(models.Model):
    """Editable homepage content blocks"""
    key = models.SlugField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.key


class NavItem(models.Model):
    """Dynamic navigation items - CMS managed"""
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500, help_text='URL path e.g. /about/ or https://...')
    icon_class = models.CharField(max_length=100, blank=True, help_text='Font Awesome e.g. fas fa-home')
    custom_icon = models.FileField(upload_to='nav_icons/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_button = models.BooleanField(default=False, help_text='Style as button (e.g. Donate)')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class SiteTheme(models.Model):
    """Singleton theme settings - colors, nav styling"""
    primary_color = models.CharField(max_length=7, default='#0B5345')
    secondary_color = models.CharField(max_length=7, default='#148f77')
    nav_bg_color = models.CharField(max_length=7, default='#0B5345')
    nav_text_color = models.CharField(max_length=7, default='#ffffff')
    nav_hover_color = models.CharField(max_length=50, default='rgba(255,255,255,0.15)')
    button_color = models.CharField(max_length=7, default='#c17f59')
    button_hover_color = models.CharField(max_length=7, default='#a86d4a')
    dark_mode_enabled = models.BooleanField(default=False, help_text='Enable dark mode for the site')
    dark_bg_color = models.CharField(max_length=7, default='#1a1a1a', help_text='Dark mode background')
    dark_text_color = models.CharField(max_length=7, default='#e0e0e0', help_text='Dark mode text')
    dark_card_bg = models.CharField(max_length=7, default='#2d2d2d', help_text='Dark mode card background')

    class Meta:
        verbose_name = 'Site theme'
        verbose_name_plural = 'Site theme'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AnnouncementPopup(models.Model):
    """Popup announcements for homepage - can include image"""
    PRIORITY_CHOICES = [('high', 'High'), ('medium', 'Medium'), ('low', 'Low')]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('expired', 'Expired'),
    ]
    title = models.CharField(max_length=200)
    message = models.TextField()
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_active = models.BooleanField(default=True)
    link_url = models.CharField(max_length=500, blank=True)
    link_text = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-start_date', '-id']

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    """Gallery images for homepage"""
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or str(self.id)


class SiteIdentity(models.Model):
    """Site identity - logo, favicon, title, tagline"""
    site_title = models.CharField(max_length=200, default='NHAF Nepal')
    tagline = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.FileField(upload_to='site/', blank=True, null=True, help_text='ICO, PNG, or SVG')

    class Meta:
        verbose_name = 'Site identity'
        verbose_name_plural = 'Site identity'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_title
