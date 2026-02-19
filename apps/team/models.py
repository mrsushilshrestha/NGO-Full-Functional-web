from django.db import models
from django.urls import reverse


class Chapter(models.Model):
    """Chapter/Location for team members"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Member(models.Model):
    """Team member directory"""
    ROLE_LEVEL_CHOICES = [
        ('executive', 'Executive'),
        ('core', 'Core'),
        ('general', 'General'),
    ]
    name = models.CharField(max_length=200)
    member_id = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=200)
    role_level = models.CharField(max_length=20, choices=ROLE_LEVEL_CHOICES, default='general')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    education = models.CharField(max_length=255, blank=True)
    join_year = models.PositiveIntegerField(blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_member_detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        parts = (self.name or '').split()
        if not parts:
            return ''
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[1][0]).upper()


class Collaboration(models.Model):
    """Collaboration / Partner Wings - MOUs, partnerships, affiliations"""
    PARTNERSHIP_TYPE_CHOICES = [
        ('mou', 'Memorandum of Understanding (MOU)'),
        ('academic', 'Academic Partner'),
        ('ngo', 'NGO Partner'),
        ('corporate', 'Corporate Partner'),
        ('government', 'Government Partner'),
        ('wing', 'Partner Wing'),
        ('strategic', 'Strategic Partner'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    BACKGROUND_COLOR_CHOICES = [
        ('', 'Default (Warm cream)'),
        ('#faf8f5', 'Cream'),
        ('#f5f2ed', 'Warm beige'),
        ('#f0f7f4', 'Mint green'),
        ('#e8f4f8', 'Soft blue'),
        ('#f8f4e8', 'Light gold'),
        ('#f5f0e8', 'Sand'),
        ('#eef5f0', 'Sage'),
    ]
    organization_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='collaborations/', blank=True, null=True)
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES, default='mou')
    short_description = models.TextField(max_length=300, help_text='Brief 2-3 line summary')
    full_description = models.TextField(blank=True, help_text='Complete description of collaboration')
    objectives = models.TextField(blank=True, help_text='Objectives and scope of partnership')
    programs_activities = models.TextField(blank=True, help_text='Programs or activities conducted')
    impact_outcomes = models.TextField(blank=True, help_text='Impact and outcomes achieved')
    agreement_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    partner_website = models.URLField(blank=True, help_text='Partner organization website')
    partner_contact = models.CharField(max_length=200, blank=True)
    mou_document = models.FileField(upload_to='collaborations/mous/', blank=True, null=True, help_text='Optional downloadable MOU file')
    supporting_images = models.ImageField(upload_to='collaborations/gallery/', blank=True, null=True, help_text='Supporting image or photo')
    detail_background_color = models.CharField(
        max_length=7, blank=True, choices=BACKGROUND_COLOR_CHOICES,
        help_text='Background color for detail page. Leave blank for default.'
    )
    detail_background_image = models.ImageField(
        upload_to='collaborations/backgrounds/',
        blank=True, null=True,
        help_text='Optional background image for detail page. Shown with subtle overlay.'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-agreement_date', 'organization_name']
        verbose_name = 'Collaboration'
        verbose_name_plural = 'Collaborations'

    def __str__(self):
        return self.organization_name

    def get_absolute_url(self):
        return reverse('collaboration_detail', kwargs={'pk': self.pk})

    def mou_is_image(self):
        """Check if MOU document is an image (JPG, PNG, etc.)"""
        if not self.mou_document:
            return False
        ext = (self.mou_document.name or '').lower().split('.')[-1]
        return ext in ('jpg', 'jpeg', 'png', 'gif', 'webp')

    def mou_is_pdf(self):
        """Check if MOU document is PDF"""
        if not self.mou_document:
            return False
        return (self.mou_document.name or '').lower().endswith('.pdf')

    def get_mou_view_url(self):
        """Return URL for MOU viewer page, or None if no document"""
        if not self.mou_document:
            return None
        return reverse('collaboration_mou_view', kwargs={'pk': self.pk})
