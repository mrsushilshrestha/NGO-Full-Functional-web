# Generated migration for hero banner display options and announcement image
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='herobanner',
            name='aspect_ratio',
            field=models.CharField(choices=[('16:9', '16:9 (Widescreen)'), ('21:9', '21:9 (Ultrawide)'), ('4:3', '4:3 (Standard)'), ('1:1', '1:1 (Square)')], default='16:9', max_length=10),
        ),
        migrations.AddField(
            model_name='herobanner',
            name='overlay_opacity',
            field=models.DecimalField(decimal_places=2, default=0.7, help_text='0=transparent, 1=solid. Dark overlay on image for text readability.', max_digits=3),
        ),
        migrations.AddField(
            model_name='herobanner',
            name='show_overlay',
            field=models.BooleanField(default=True, help_text='Show dark overlay on image'),
        ),
        migrations.AddField(
            model_name='herobanner',
            name='image_fit',
            field=models.CharField(choices=[('cover', 'Cover (Fill)'), ('contain', 'Contain (Fit)')], default='cover', max_length=10),
        ),
        migrations.AddField(
            model_name='herobanner',
            name='text_position',
            field=models.CharField(choices=[('center', 'Center'), ('left', 'Left'), ('right', 'Right')], default='center', max_length=10),
        ),
        migrations.AddField(
            model_name='announcementpopup',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='announcements/'),
        ),
    ]
