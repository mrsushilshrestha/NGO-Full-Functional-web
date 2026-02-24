# Migration: SMS Settings and Message Templates for application notifications

from django.db import migrations, models


def create_default_sms_templates(apps, schema_editor):
    """Create default SMS message templates for application workflow."""
    SMSMessageTemplate = apps.get_model('cms', 'SMSMessageTemplate')
    defaults = [
        ('received', 'Thank you. We have received your application and it is under review.'),
        ('approved', 'Congratulations! Your application has been approved.'),
        ('rejected', 'We regret to inform you that your application has been rejected.'),
    ]
    for ttype, msg in defaults:
        SMSMessageTemplate.objects.get_or_create(
            template_type=ttype,
            defaults={'message': msg, 'is_active': True}
        )


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_create_default_icons'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(blank=True, help_text='Email address used to send SMS (for email-to-SMS gateways). Example: notifications@xyz.org', max_length=254)),
                ('sender_id', models.CharField(blank=True, help_text='Sender ID shown on recipient phone (provider-dependent)', max_length=50)),
                ('api_key', models.CharField(blank=True, help_text='SMS Gateway API Key', max_length=255)),
                ('api_secret', models.CharField(blank=True, help_text='API Secret (if required by provider)', max_length=255)),
                ('endpoint_url', models.URLField(blank=True, help_text='API endpoint URL (optional - some providers use fixed URLs)')),
                ('sms_enabled', models.BooleanField(default=False, help_text='Enable SMS notifications')),
            ],
            options={
                'verbose_name': 'SMS Settings',
                'verbose_name_plural': 'SMS Settings',
            },
        ),
        migrations.CreateModel(
            name='SMSMessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('received', 'Form Submission (Received)'), ('approved', 'Application Approved'), ('rejected', 'Application Rejected')], max_length=20, unique=True)),
                ('subject', models.CharField(blank=True, help_text='Optional subject (for email gateways)', max_length=200)),
                ('message', models.TextField(default='Thank you. We have received your application and it is under review.', help_text='SMS content. Placeholders: {name}, {application_type}, {date}')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'SMS Message Template',
                'verbose_name_plural': 'SMS Message Templates',
            },
        ),
        migrations.RunPython(create_default_sms_templates, reverse_noop),
    ]
