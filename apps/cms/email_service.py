"""
Email notification service for application workflow.
Uses CMS EmailSettings (SMTP when configured). Only sends if sender_email is set. Fails gracefully.
"""
import logging
from django.core.mail import get_connection, EmailMessage

logger = logging.getLogger(__name__)


def send_application_email(to_email: str, subject: str, body: str, template_type: str = '') -> bool:
    """
    Send email to applicant. Uses SMTP from EmailSettings when smtp_host is set.
    Returns True if sent or skipped safely. Does NOT send if sender_email is not configured.
    """
    try:
        from .models import EmailSettings
        settings = EmailSettings.get()
        if not settings.email_enabled or not settings.sender_email or not str(settings.sender_email).strip():
            logger.debug('Email not configured (no sender), skipping.')
            return True
        if not to_email or not str(to_email).strip():
            return False
        from_email = f'{settings.sender_name or "NHAF"} <{settings.sender_email}>'
        recipient = str(to_email).strip()

        if getattr(settings, 'smtp_host', None) and str(settings.smtp_host).strip():
            port = getattr(settings, 'smtp_port', None) or 587
            use_tls = getattr(settings, 'smtp_use_tls', True)
            conn = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=settings.smtp_host.strip(),
                port=port,
                username=(getattr(settings, 'smtp_username', None) or '').strip() or None,
                password=(getattr(settings, 'smtp_password', None) or '').strip() or None,
                use_tls=use_tls,
                fail_silently=True,
            )
            msg = EmailMessage(subject=subject, body=body, from_email=from_email, to=[recipient], connection=conn)
            msg.send(fail_silently=True)
        else:
            from django.core.mail import send_mail
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[recipient],
                fail_silently=True,
            )
        return True
    except Exception as e:
        logger.exception('Email send failed: %s', e)
        return False


def get_email_template_message(template_type: str, context: dict) -> tuple:
    """Return (subject, body) from EmailMessageTemplate or defaults. Injects organization_name, contact_info from EmailSettings."""
    from .models import EmailMessageTemplate, EmailSettings
    ctx = dict(context)
    try:
        email_settings = EmailSettings.get()
        ctx.setdefault('organization_name', getattr(email_settings, 'organization_name', '') or 'NHAF Nepal')
        ctx.setdefault('contact_info', getattr(email_settings, 'contact_info', '') or '')
    except Exception:
        ctx.setdefault('organization_name', 'NHAF Nepal')
        ctx.setdefault('contact_info', '')
    tpl = EmailMessageTemplate.objects.filter(template_type=template_type, is_active=True).first()
    if not tpl:
        defaults = {
            'received': ('Application Received', 'Dear {name},\n\nThank you. We have received your application and it is under review.\n\nThank you,\n{organization_name}'),
            'approved': ('Application Approved', 'Dear {name},\n\nCongratulations! Your application has been approved.\n\nThank you,\n{organization_name}'),
            'rejected': ('Application Update', 'Dear {name},\n\nWe regret to inform you that your application was not approved at this time.\n\nThank you,\n{organization_name}'),
        }
        subj, body = defaults.get(template_type, ('', ''))
        for k, v in ctx.items():
            body = body.replace('{' + k + '}', str(v or ''))
        return (subj, body)
    return (tpl.subject, tpl.render(ctx))
