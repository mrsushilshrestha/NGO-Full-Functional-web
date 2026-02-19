"""Create CMS notifications when events occur."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CMSNotification
from apps.contact.models import ContactMessage
from apps.membership.models import VolunteerApplication, MembershipApplication
from apps.donation.models import Donation
from apps.team.models import Member


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
            message=f'{instance.location} - Pending approval',
            link='/admin-login/members/',
        )
    elif instance.status == 'approved':
        # Create or update a public Member entry for approved volunteers
        member_defaults = {
            'name': instance.name,
            'role': 'Volunteer',
            'role_level': 'general',
            'email': getattr(instance, 'email', '') or '',
            'phone': instance.contact_number,
            'is_active': True,
        }
        if getattr(instance, 'profile_image', None):
            member_defaults['photo'] = instance.profile_image
        Member.objects.update_or_create(
            email=member_defaults['email'] or None,
            defaults=member_defaults,
        )
        CMSNotification.objects.create(
            notification_type='member_approved',
            title=f'Volunteer approved: {instance.name}',
            message='Volunteer application has been approved and published to the team directory.',
            link='/admin-login/member-management/',
        )


@receiver(post_save, sender=MembershipApplication)
def notify_membership(sender, instance, created, **kwargs):
    if created:
        CMSNotification.objects.create(
            notification_type='member_pending',
            title=f'New membership: {instance.name}',
            message=f'{instance.get_member_type_display()} - Pending approval',
            link='/admin-login/members/',
        )
    elif instance.status == 'approved':
        # Map membership type to a Member role/level
        if instance.member_type == 'general':
            role = 'General Member'
            role_level = 'general'
        else:
            role = 'Active Member'
            role_level = 'general'

        Member.objects.update_or_create(
            email=instance.email,
            defaults={
                'name': instance.name,
                'role': role,
                'role_level': role_level,
                'email': instance.email,
                'phone': instance.phone,
                'is_active': True,
            },
        )
        CMSNotification.objects.create(
            notification_type='member_approved',
            title=f'Member approved: {instance.name}',
            message='Membership application has been approved and published to the team directory.',
            link='/admin-login/member-management/',
        )


@receiver(post_save, sender=Donation)
def notify_donation(sender, instance, created, **kwargs):
    if created and instance.status == 'completed':
        CMSNotification.objects.create(
            notification_type='payment_received',
            title=f'Donation received: NPR {instance.amount}',
            message=f'From {instance.donor_name or "Anonymous"}',
            link='/admin-login/donation/',
        )
