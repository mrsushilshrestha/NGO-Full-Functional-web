# Join Us section (TeamPageSettings) + Member.twitter_url

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('team', '0012_member_volunteer_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='twitter_url',
            field=models.URLField(blank=True, help_text='Twitter/X profile URL'),
        ),
        migrations.AddField(
            model_name='teampagesettings',
            name='join_us_description',
            field=models.TextField(blank=True, default='', help_text='Optional longer description. Shown below subtitle on the Join Us card.'),
        ),
        migrations.AddField(
            model_name='teampagesettings',
            name='join_us_image',
            field=models.ImageField(blank=True, help_text='Main image for the Join Us card. Recommended size: 600×400px or similar.', null=True, upload_to='team/join_us/'),
        ),
        migrations.AddField(
            model_name='teampagesettings',
            name='join_us_subtitle',
            field=models.CharField(default='Collaborate with the best talent in the industry. Your journey starts right here.', help_text='Subtitle or tagline below the title.', max_length=300),
        ),
        migrations.AddField(
            model_name='teampagesettings',
            name='join_us_title',
            field=models.CharField(default='Join Our Community', help_text='Main title for the Join Us section.', max_length=200),
        ),
    ]
