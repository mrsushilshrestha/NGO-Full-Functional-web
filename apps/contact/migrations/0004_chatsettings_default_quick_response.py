from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('contact', '0003_chatsettings_admin_last_seen')]

    operations = [
        migrations.AddField(
            model_name='chatsettings',
            name='default_quick_response',
            field=models.ForeignKey(
                blank=True, help_text='If set, this message is sent as auto-reply instead of the text below.',
                null=True, on_delete=django.db.models.deletion.SET_NULL, to='contact.quickresponse'
            ),
        ),
    ]
