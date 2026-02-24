# Migration: EmailSettings SMTP + branding; EmailMessageTemplate footer

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('cms', '0005_email_settings_and_templates')]

    operations = [
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_host',
            field=models.CharField(blank=True, help_text='SMTP server host (e.g. smtp.gmail.com)', max_length=255),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_port',
            field=models.PositiveIntegerField(blank=True, default=587, help_text='SMTP port (e.g. 587 for TLS)', null=True),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_use_tls',
            field=models.BooleanField(default=True, help_text='Use TLS for SMTP'),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_username',
            field=models.CharField(blank=True, help_text='SMTP username or email', max_length=255),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='smtp_password',
            field=models.CharField(blank=True, help_text='SMTP password or app password', max_length=255),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='organization_name',
            field=models.CharField(blank=True, default='NHAF Nepal', help_text='Used in templates as {organization_name}', max_length=200),
        ),
        migrations.AddField(
            model_name='emailsettings',
            name='contact_info',
            field=models.TextField(blank=True, help_text='Footer/contact details (e.g. phone, address). Used as {contact_info} in templates.'),
        ),
        migrations.AddField(
            model_name='emailmessagetemplate',
            name='footer',
            field=models.TextField(blank=True, help_text='Optional footer (e.g. Thank you, {organization_name}. Placeholders: {organization_name}, {contact_info})'),
        ),
    ]
