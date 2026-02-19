from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('contact', '0004_chatsettings_default_quick_response')]

    operations = [
        migrations.AddField(
            model_name='quickresponse',
            name='trigger_keywords',
            field=models.CharField(
                blank=True,
                help_text="Comma-separated keywords. If set, this response is sent only when the user's first message contains any of these (case-insensitive). Leave empty to use as default first-message reply.",
                max_length=500,
            ),
        ),
        migrations.AddField(
            model_name='chatsettings',
            name='chat_mode',
            field=models.CharField(
                choices=[
                    ('builtin', 'Built-in live chat'),
                    ('whatsapp', 'WhatsApp (recommended)'),
                    ('custom', 'Custom link (Telegram, etc.)'),
                ],
                default='builtin',
                help_text='Use built-in chat, WhatsApp, or a custom chat link.',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='chatsettings',
            name='whatsapp_phone',
            field=models.CharField(
                blank=True,
                help_text='WhatsApp number with country code, no + or spaces (e.g. 9779812345678).',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='chatsettings',
            name='custom_chat_link',
            field=models.URLField(
                blank=True,
                help_text='For "Custom link": full URL (e.g. Telegram, Messenger).',
            ),
        ),
    ]
