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


class SMSSettings(models.Model):
    """
    CMS-editable SMS gateway configuration.
    Supports various providers (Twilio, custom APIs, email-to-SMS gateways).
    """
    # Sender / From configuration
    sender_email = models.EmailField(blank=True, help_text='Email address used to send SMS (for email-to-SMS gateways). Example: notifications@xyz.org')
    sender_id = models.CharField(max_length=50, blank=True, help_text='Sender ID shown on recipient phone (provider-dependent)')
    # API credentials
    api_key = models.CharField(max_length=255, blank=True, help_text='SMS Gateway API Key')
    api_secret = models.CharField(max_length=255, blank=True, help_text='API Secret (if required by provider)')
    endpoint_url = models.URLField(blank=True, help_text='API endpoint URL (optional - some providers use fixed URLs)')
    # Enable/disable
    sms_enabled = models.BooleanField(default=False, help_text='Enable SMS notifications')
    # Singleton - one config per site
    class Meta:
        verbose_name = 'SMS Settings'
        verbose_name_plural = 'SMS Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SMSMessageTemplate(models.Model):
    """
    Editable SMS message templates for application workflow.
    Placeholders: {name}, {application_type}, {date}
    """
    TEMPLATE_TYPE_CHOICES = [
        ('received', 'Form Submission (Received)'),
        ('approved', 'Application Approved'),
        ('rejected', 'Application Rejected'),
    ]
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, unique=True)
    subject = models.CharField(max_length=200, blank=True, help_text='Optional subject (for email gateways)')
    message = models.TextField(
        help_text='SMS content. Placeholders: {name}, {application_type}, {date}',
        default='Thank you. We have received your application and it is under review.',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'SMS Message Template'
        verbose_name_plural = 'SMS Message Templates'

    def __str__(self):
        return self.get_template_type_display()

    def render(self, context):
        """Replace placeholders with context values."""
        msg = self.message
        for key, val in context.items():
            msg = msg.replace('{' + key + '}', str(val or ''))
        return msg


class EmailSettings(models.Model):
    """CMS-editable email configuration for application notifications."""
    sender_email = models.EmailField(blank=True, help_text='From address. If empty, no emails are sent.')
    sender_name = models.CharField(max_length=100, blank=True, default='NHAF Nepal')
    email_enabled = models.BooleanField(default=False)
    # SMTP / service configuration (optional; if not set, Django default backend may be used)
    smtp_host = models.CharField(max_length=255, blank=True, help_text='SMTP server host (e.g. smtp.gmail.com)')
    smtp_port = models.PositiveIntegerField(default=587, blank=True, null=True, help_text='SMTP port (e.g. 587 for TLS)')
    smtp_use_tls = models.BooleanField(default=True, help_text='Use TLS for SMTP')
    smtp_username = models.CharField(max_length=255, blank=True, help_text='SMTP username or email')
    smtp_password = models.CharField(max_length=255, blank=True, help_text='SMTP password or app password')
    # Branding for email templates
    organization_name = models.CharField(max_length=200, blank=True, default='NHAF Nepal', help_text='Used in templates as {organization_name}')
    contact_info = models.TextField(blank=True, help_text='Footer/contact details (e.g. phone, address). Used as {contact_info} in templates.')

    class Meta:
        verbose_name = 'Email Settings'
        verbose_name_plural = 'Email Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class EmailMessageTemplate(models.Model):
    """Editable email templates for application workflow. Placeholders: {name}, {application_type}, {date}, {organization_name}, {contact_info}."""
    TEMPLATE_TYPE_CHOICES = [
        ('received', 'Form Received'),
        ('approved', 'Application Approved'),
        ('rejected', 'Application Rejected'),
    ]
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, unique=True)
    subject = models.CharField(max_length=300, help_text='Email subject line')
    body = models.TextField(help_text='Main message. Placeholders: {name}, {application_type}, {date}, {organization_name}')
    footer = models.TextField(blank=True, help_text='Optional footer (e.g. Thank you, {organization_name}. Placeholders: {organization_name}, {contact_info})')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Email Message Template'
        verbose_name_plural = 'Email Message Templates'

    def __str__(self):
        return self.get_template_type_display()

    def render(self, context):
        text = self.body
        for k, v in context.items():
            text = text.replace('{' + k + '}', str(v or ''))
        if self.footer:
            footer_text = self.footer
            for k, v in context.items():
                footer_text = footer_text.replace('{' + k + '}', str(v or ''))
            text = text.rstrip() + '\n\n' + footer_text
        return text


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
