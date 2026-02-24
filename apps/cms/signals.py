"""Create CMS notifications when events occur. Also triggers SMS notifications."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import CMSNotification
from apps.contact.models import ContactMessage
from apps.membership.models import VolunteerApplication, MembershipApplication
from apps.donation.models import Donation
from apps.team.models import Member


def _send_application_sms(phone_value, name, application_type, template_type):
    """Helper: send SMS for application workflow using CMS templates."""
    try:
        from .sms_service import send_sms, get_template_message
        phone = str(phone_value).strip() if phone_value else ''
        if not phone:
            return
        ctx = {
            'name': name or '',
            'application_type': application_type or '',
            'date': timezone.now().strftime('%Y-%m-%d'),
        }
        msg = get_template_message(template_type, ctx)
        if msg:
            send_sms(phone, msg, application_type)
    except Exception:
        pass  # Don't break main flow if SMS fails


def _send_application_email(email_value, name, application_type, template_type):
    """Helper: send email for application workflow. No sender = no send, no errors."""
    try:
        from .email_service import send_application_email, get_email_template_message
        email = str(email_value).strip() if email_value else ''
        if not email:
            return
        ctx = {
            'name': name or '',
            'application_type': application_type or '',
            'date': timezone.now().strftime('%Y-%m-%d'),
        }
        subj, body = get_email_template_message(template_type, ctx)
        if subj and body:
            send_application_email(email, subj, body, template_type)
    except Exception:
        pass  # Graceful - never break main flow


@receiver(post_save, sender=ContactMessage)
def notify_contact_message(sender, instance, created, **kwargs):
    if created:
        CMSNotification.objects.create(
            notification_type='contact_message',
            title=f'New message from {instance.name}',
            message=instance.subject or instance.message[:100],
            link='/admin-login/contact/',
        )


@receiver(post_save, sender=VolunteerApplication)
def notify_volunteer(sender, instance, created, **kwargs):
    if created:
        CMSNotification.objects.create(
            notification_type='volunteer_pending',
            title=f'New volunteer: {instance.name}',
            message=f'{getattr(instance.district, "name", None) or instance.location or "N/A"} - Pending approval',
            link='/admin-login/members/',
        )
        _send_application_sms(instance.contact_number, instance.name, 'Volunteer', 'received')
        _send_application_email(instance.email, instance.name, 'Volunteer', 'received')
    elif instance.status == 'approved':
        # Create or update exactly one Member per approved application (by linking to VolunteerApplication).
        # This prevents overwriting other volunteers when email is empty or duplicated.
        member_defaults = {
            'name': instance.name,
            'role': 'Volunteer',
            'member_type': 'volunteer',
            'email': getattr(instance, 'email', '') or '',
            'phone': instance.contact_number,
            'is_active': True,
            'district': getattr(instance, 'district', None),
            'exclude_from_public': False,
            'facebook_url': getattr(instance, 'facebook_url', '') or '',
            'instagram_url': getattr(instance, 'instagram_url', '') or '',
            'linkedin_url': getattr(instance, 'linkedin_url', '') or '',
            'twitter_url': getattr(instance, 'twitter_url', '') or '',
        }
        if getattr(instance, 'profile_image', None):
            member_defaults['photo'] = instance.profile_image
        member, created = Member.objects.update_or_create(
            volunteer_application=instance,
            defaults=member_defaults,
        )
        if not member.member_id or (member.member_id or '').strip() == '':
            member.member_id = member.generate_member_id()
            member.save(update_fields=['member_id'])
        CMSNotification.objects.create(
            notification_type='member_approved',
            title=f'Volunteer approved: {instance.name}',
            message='Volunteer application has been approved and published to the team directory.',
            link='/admin-login/member-management/',
        )
        _send_application_sms(instance.contact_number, instance.name, 'Volunteer', 'approved')
        _send_application_email(instance.email, instance.name, 'Volunteer', 'approved')
    elif instance.status == 'rejected':
        # Hide the Member from the public site if one was created for this application
        try:
            m = Member.objects.filter(volunteer_application=instance).first()
            if m:
                m.exclude_from_public = True
                m.is_active = False
                m.save(update_fields=['exclude_from_public', 'is_active'])
        except Exception:
            pass
        _send_application_sms(instance.contact_number, instance.name, 'Volunteer', 'rejected')
        _send_application_email(instance.email, instance.name, 'Volunteer', 'rejected')


@receiver(post_save, sender=MembershipApplication)
def notify_membership(sender, instance, created, **kwargs):
    if created:
        CMSNotification.objects.create(
            notification_type='member_pending',
            title=f'New membership: {instance.name}',
            message=f'{instance.get_member_type_display()} - Pending approval',
            link='/admin-login/members/',
        )
        _send_application_sms(instance.phone, instance.name, 'Membership', 'received')
        _send_application_email(instance.email, instance.name, 'Membership', 'received')
    elif instance.status == 'approved':
        # Map membership application to Volunteer member type
        member, created = Member.objects.update_or_create(
            email=instance.email,
            defaults={
                'name': instance.name,
                'role': 'Volunteer',
                'member_type': 'volunteer',
                'email': instance.email,
                'phone': instance.phone,
                'is_active': True,
                'exclude_from_public': True,  # Hide members from paid membership (bank amount)
            },
        )
        # Ensure member_id is generated if missing
        if not member.member_id or member.member_id.strip() == '':
            member.member_id = member.generate_member_id()
            member.save(update_fields=['member_id'])
        CMSNotification.objects.create(
            notification_type='member_approved',
            title=f'Member approved: {instance.name}',
            message='Membership application has been approved and published to the team directory.',
            link='/admin-login/member-management/',
        )
        _send_application_sms(instance.phone, instance.name, 'Membership', 'approved')
        _send_application_email(instance.email, instance.name, 'Membership', 'approved')
    elif instance.status == 'rejected':
        _send_application_sms(instance.phone, instance.name, 'Membership', 'rejected')
        _send_application_email(instance.email, instance.name, 'Membership', 'rejected')


@receiver(post_save, sender=Donation)
def notify_donation(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        CMSNotification.objects.create(
            notification_type='payment_received',
            title=f'Donation received: NPR {instance.amount}',
            message=f'From {instance.donor_name or "Anonymous"}',
            link='/admin-login/donation/',
        )
