"""Context processors for CMS - notification count in header."""
from django.db import OperationalError

from .models import CMSNotification


def cms_notifications(request):
    """Add notification count for CMS pages."""
    if request.path.startswith('/admin-login/') and request.user.is_authenticated and request.user.is_staff:
        try:
            return {'cms_unread_count': CMSNotification.objects.filter(is_read=False).count()}
        except OperationalError:
            return {'cms_unread_count': 0}
    return {'cms_unread_count': 0}
