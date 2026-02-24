# VolunteerApplication - social media link fields

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0003_volunteerapplication_cv_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerapplication',
            name='facebook_url',
            field=models.URLField(blank=True, help_text='Facebook profile URL'),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='instagram_url',
            field=models.URLField(blank=True, help_text='Instagram profile URL'),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='linkedin_url',
            field=models.URLField(blank=True, help_text='LinkedIn profile URL'),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='twitter_url',
            field=models.URLField(blank=True, help_text='Twitter/X profile URL'),
        ),
    ]
