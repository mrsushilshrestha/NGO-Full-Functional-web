from django.db import models


class ContactInfo(models.Model):
    """Contact information - CMS editable"""
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    office_hours = models.CharField(max_length=200, blank=True)
    map_embed = models.TextField(blank=True, help_text='Google Maps embed code for New Baneshwor, Kathmandu')

    class Meta:
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return 'Contact Info'


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class ChatMessage(models.Model):
    """Live chat messages between users and admins"""
    SENDER_CHOICES = [('user', 'User'), ('admin', 'Admin')]
    session_id = models.CharField(max_length=100, db_index=True, help_text='Unique session identifier for user')
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    sender_name = models.CharField(max_length=200, blank=True)
    sender_email = models.EmailField(blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender_type}: {self.message[:50]}'


class QuickResponse(models.Model):
    """Predefined quick response messages for live chat. Only used for the first message in a conversation."""
    message = models.TextField(help_text='Quick response text')
    trigger_keywords = models.CharField(
        max_length=500, blank=True,
        help_text='Comma-separated keywords. If set, this response is sent only when the user\'s first message contains any of these (case-insensitive). Leave empty to use as default first-message reply.'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.message[:50]

    def message_matches(self, user_message):
        if not self.trigger_keywords.strip():
            return True
        msg_lower = (user_message or '').lower()
        for kw in self.trigger_keywords.split(','):
            if kw.strip().lower() in msg_lower:
                return True
        return False


class ChatSettings(models.Model):
    """Live chat system settings"""
    CHAT_MODE_BUILTIN = 'builtin'
    CHAT_MODE_WHATSAPP = 'whatsapp'
    CHAT_MODE_CUSTOM = 'custom'
    CHAT_MODE_CHOICES = [
        (CHAT_MODE_BUILTIN, 'Built-in live chat'),
        (CHAT_MODE_WHATSAPP, 'WhatsApp (recommended)'),
        (CHAT_MODE_CUSTOM, 'Custom link (Telegram, etc.)'),
    ]
    is_enabled = models.BooleanField(default=True)
    chat_mode = models.CharField(
        max_length=20, choices=CHAT_MODE_CHOICES, default=CHAT_MODE_BUILTIN,
        help_text='Use built-in chat, WhatsApp, or a custom chat link.'
    )
    whatsapp_phone = models.CharField(
        max_length=20, blank=True,
        help_text='WhatsApp number with country code, no + or spaces (e.g. 9779812345678). Used to build wa.me link.'
    )
    custom_chat_link = models.URLField(
        blank=True,
        help_text='For "Custom link": full URL (e.g. Telegram, Messenger, or any chat app link).'
    )
    auto_response_enabled = models.BooleanField(default=False)
    default_quick_response = models.ForeignKey(
        QuickResponse, null=True, blank=True, on_delete=models.SET_NULL,
        help_text='If set, this message is sent as auto-reply instead of the text below.'
    )
    auto_response_message = models.TextField(default='Thank you for contacting us. Our team will respond shortly.')
    admin_last_seen = models.DateTimeField(null=True, blank=True, help_text='Last time admin was on chat page')

    class Meta:
        verbose_name = 'Chat settings'
        verbose_name_plural = 'Chat settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def admin_is_online(self, minutes=5):
        from django.utils import timezone
        if not self.admin_last_seen:
            return False
        return (timezone.now() - self.admin_last_seen).total_seconds() < minutes * 60
