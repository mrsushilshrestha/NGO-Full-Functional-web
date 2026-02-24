# Generated manually - extend BlogPageSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpagesettings',
            name='banner_image',
            field=models.ImageField(blank=True, help_text='Optional hero banner image (uses default if empty)', null=True, upload_to='blog/banner/'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='posts_per_page',
            field=models.PositiveIntegerField(default=9, help_text='Number of posts per page'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='enable_featured_layout',
            field=models.BooleanField(default=False, help_text='Show one post as large featured card above the grid'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='default_sort',
            field=models.CharField(
                choices=[('latest', 'Latest first'), ('oldest', 'Oldest first')],
                default='latest',
                help_text='Default sort order',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='seo_title',
            field=models.CharField(blank=True, help_text='SEO meta title for blog listing page', max_length=200),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='seo_description',
            field=models.TextField(blank=True, help_text='SEO meta description for blog listing page', max_length=320),
        ),
        migrations.AlterField(
            model_name='blogpagesettings',
            name='hero_title',
            field=models.CharField(
                default='Blog',
                help_text='Page title (e.g. Blog, Stories from the Field)',
                max_length=200
            ),
        ),
    ]
