# Generated manually for blog app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(blank=True, help_text='e.g. Health Officer, Field Coordinator', max_length=200)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='blog/authors/')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Blog categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='BlogPageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title', models.CharField(default='Stories from the Field', help_text='Large hero title on blog listing', max_length=200)),
                ('hero_subtitle', models.TextField(blank=True, default='Read about our health outreach, community programs, and impact across Nepal.', help_text='Subtitle describing the NGO work and impact')),
            ],
            options={
                'verbose_name': 'Blog page settings',
                'verbose_name_plural': 'Blog page settings',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=300, unique=True)),
                ('title', models.CharField(max_length=400)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20)),
                ('author_name', models.CharField(blank=True, max_length=200)),
                ('author_role', models.CharField(blank=True, max_length=200)),
                ('author_avatar', models.ImageField(blank=True, null=True, upload_to='blog/authors/')),
                ('excerpt', models.TextField(help_text='Short excerpt for listing cards', max_length=300)),
                ('long_excerpt', models.TextField(blank=True, help_text='Long intro paragraph for detail page')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('image_caption', models.CharField(blank=True, max_length=400)),
                ('featured', models.BooleanField(default=False, help_text='Show as featured post on listing')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(blank=True, help_text='Leave blank to use author name/role/avatar below', null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.blogauthor')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.blogcategory')),
                ('tags', models.ManyToManyField(blank=True, to='blog.blogtag')),
            ],
            options={
                'ordering': ['-date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BlogContentBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('paragraph', 'Paragraph'), ('heading', 'Heading'), ('quote', 'Quote'), ('list', 'Bulleted List')], max_length=20)),
                ('content', models.TextField(blank=True)),
                ('attribution', models.CharField(blank=True, help_text='For quotes: attribution line', max_length=300)),
                ('order', models.PositiveIntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_blocks', to='blog.blogpost')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]
