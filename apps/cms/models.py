"""CMS models - Notifications and system config."""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CMSNotification(models.Model):
    """Notifications for CMS admin users."""
    TYPE_CHOICES = [
        ('member_pending', 'Member Pending'),
        ('member_approved', 'Member Approved'),
        ('member_rejected', 'Member Rejected'),
        ('payment_received', 'Payment Received'),
        ('contact_message', 'Contact Message'),
        ('volunteer_pending', 'Volunteer Pending'),
        ('system', 'System Alert'),
    ]
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True, help_text='Link path e.g. /admin-login/contact/')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class IconConfig(models.Model):
    """Icon assignments for menus, buttons, sections - editable from CMS."""
    LOCATION_CHOICES = [
        ('nav_home', 'Nav: Home'),
        ('nav_about', 'Nav: About'),
        ('nav_programs', 'Nav: Programs'),
        ('nav_team', 'Nav: Team'),
        ('nav_impact', 'Nav: Impact'),
        ('nav_contact', 'Nav: Contact'),
        ('nav_donate', 'Nav: Donate'),
    ]
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, unique=True)
    icon_class = models.CharField(max_length=100, default='fas fa-circle',
        help_text='Font Awesome class e.g. fas fa-home')
    custom_svg = models.FileField(upload_to='icons/', blank=True, null=True)

    def __str__(self):
        return self.get_location_display()
