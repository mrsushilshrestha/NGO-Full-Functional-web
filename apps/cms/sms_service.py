"""
SMS Notification Service for application workflow.
Supports configurable gateways (Twilio, custom APIs, email-to-SMS).
Admin configures API key, endpoint, sender ID via CMS.
"""
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_sms(phone: str, message: str, application_type: str = '') -> bool:
    """
    Send SMS to the given phone number.
    Uses SMSSettings from CMS. Returns True if sent successfully (or skipped safely).
    """
    from .models import SMSSettings
    try:
        settings = SMSSettings.get()
        if not settings.sms_enabled:
            logger.debug('SMS disabled in settings, skipping.')
            return True  # Not an error - just disabled
        if not phone or not message or not message.strip():
            return False
        # Normalize phone - ensure +977 for Nepal
        phone = str(phone).strip().replace(' ', '')
        if not phone.startswith('+'):
            if phone.startswith('97'):
                phone = '+' + phone
            elif len(phone) == 10 and phone.isdigit():
                phone = '+977' + phone
            else:
                phone = '+977' + phone.lstrip('0')
        # Call provider-specific sender
        return _send_via_provider(settings, phone, message, application_type)
    except Exception as e:
        logger.exception('SMS send failed: %s', e)
        return False


def _send_via_provider(settings, phone: str, message: str, application_type: str) -> bool:
    """
    Dispatch to configured provider.
    If endpoint_url is set, assume HTTP POST API.
    Otherwise, if sender_email is set, could use email-to-SMS (would need backend).
    For now: log and return True when no real gateway is configured (graceful fallback).
    """
    # If API key and endpoint are configured, attempt HTTP API
    if settings.api_key and settings.endpoint_url:
        return _send_via_http_api(settings, phone, message)
    # Email-to-SMS: Some gateways accept email -> SMS (e.g. number@carrier.gateway.com)
    # Would require django email backend; defer full implementation
    if settings.sender_email and not settings.api_key:
        logger.info('SMS (email gateway): would send to %s: %s', phone, message[:50] + '...')
        return True  # Graceful skip when no backend implemented
    # No gateway configured - log and skip
    logger.info('SMS not configured. Would send to %s: %s', phone, message[:80])
    return True


def _send_via_http_api(settings, phone: str, message: str) -> bool:
    """Send via HTTP POST to configured endpoint (generic REST API pattern)."""
    try:
        import urllib.request
        import urllib.parse
        import json
        data = {
            'phone': phone,
            'message': message,
            'sender_id': settings.sender_id or '',
            'api_key': settings.api_key,
        }
        if settings.api_secret:
            data['api_secret'] = settings.api_secret
        body = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            settings.endpoint_url,
            data=body,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if 200 <= resp.status < 300:
                return True
            logger.warning('SMS API returned %s', resp.status)
            return False
    except Exception as e:
        logger.exception('SMS HTTP API error: %s', e)
        return False


def get_template_message(template_type: str, context: dict) -> str:
    """Get rendered message from SMSMessageTemplate for given type."""
    from .models import SMSMessageTemplate
    tpl = SMSMessageTemplate.objects.filter(template_type=template_type, is_active=True).first()
    if not tpl:
        defaults = {
            'received': 'Thank you. We have received your application and it is under review.',
            'approved': 'Congratulations! Your application has been approved.',
            'rejected': 'We regret to inform you that your application has been rejected.',
        }
        return defaults.get(template_type, '')
    return tpl.render(context)
