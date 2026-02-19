from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0004_default_nav_and_announcement_status')]

    operations = [
        migrations.CreateModel(
            name='SiteIdentity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(default='NHAF Nepal', max_length=200)),
                ('tagline', models.CharField(blank=True, max_length=300)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site/')),
                ('favicon', models.FileField(blank=True, help_text='ICO, PNG, or SVG', null=True, upload_to='site/')),
            ],
            options={'verbose_name': 'Site identity', 'verbose_name_plural': 'Site identity'},
        ),
        migrations.AddField(
            model_name='galleryimage',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='gallery_images', to='programs.program'),
        ),
    ]
