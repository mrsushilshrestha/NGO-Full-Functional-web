# Generated manually - swipe effect, auto search, tag popular

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpagesettings_extended'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogtag',
            name='is_popular',
            field=models.BooleanField(default=False, help_text='Show in popular tags filter'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='enable_swipe_effect',
            field=models.BooleanField(default=True, help_text='Swipe/slide card image to reveal title'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='enable_auto_search',
            field=models.BooleanField(default=True, help_text='Show real-time search suggestions'),
        ),
    ]
