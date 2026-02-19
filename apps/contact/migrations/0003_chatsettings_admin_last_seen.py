from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('contact', '0002_chat_system')]

    operations = [
        migrations.AddField(
            model_name='chatsettings',
            name='admin_last_seen',
            field=models.DateTimeField(blank=True, help_text='Last time admin was on chat page', null=True),
        ),
    ]
