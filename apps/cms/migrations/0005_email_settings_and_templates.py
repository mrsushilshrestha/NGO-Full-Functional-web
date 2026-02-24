# Migration: EmailSettings, EmailMessageTemplate

from django.db import migrations, models


def create_default_email_templates(apps, schema_editor):
    EmailMessageTemplate = apps.get_model('cms', 'EmailMessageTemplate')
    defaults = [
        ('received', 'Application Received', 'Thank you. We have received your application and it is under review.'),
        ('approved', 'Application Approved', 'Congratulations! Your application has been approved.'),
        ('rejected', 'Application Update', 'We regret to inform you that your application was not approved.'),
    ]
    for ttype, subj, body in defaults:
        EmailMessageTemplate.objects.get_or_create(
            template_type=ttype,
            defaults={'subject': subj, 'body': body, 'is_active': True}
        )


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('cms', '0004_add_sms_settings_and_templates')]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(blank=True, help_text='From address. If empty, no emails are sent.', max_length=254)),
                ('sender_name', models.CharField(blank=True, default='NHAF Nepal', max_length=100)),
                ('email_enabled', models.BooleanField(default=False)),
            ],
            options={'verbose_name': 'Email Settings', 'verbose_name_plural': 'Email Settings'},
        ),
        migrations.CreateModel(
            name='EmailMessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(choices=[('received', 'Form Received'), ('approved', 'Application Approved'), ('rejected', 'Application Rejected')], max_length=20, unique=True)),
                ('subject', models.CharField(max_length=300)),
                ('body', models.TextField(help_text='Placeholders: {name}, {application_type}, {date}')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Email Message Template', 'verbose_name_plural': 'Email Message Templates'},
        ),
        migrations.RunPython(create_default_email_templates, reverse_noop),
    ]
