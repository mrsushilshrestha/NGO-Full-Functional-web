# Generated manually for SplashScreenSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_sitetheme_show_nav_arrows'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplashScreenSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=False, help_text='Enable splash screen on homepage')),
                ('show_only_first_visit', models.BooleanField(default=True, help_text='Show only on first visit per session (recommended). Uncheck to show every visit.')),
                ('click_to_skip', models.BooleanField(default=True, help_text='Allow clicking anywhere to skip')),
                ('z_index', models.PositiveIntegerField(default=99999, help_text='Layer priority (higher = on top)')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='splash/')),
                ('background_color', models.CharField(default='#0B5345', help_text='Used when no background image', max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='splash/')),
                ('title_text', models.CharField(blank=True, default='Welcome', max_length=200)),
                ('subtitle_text', models.TextField(blank=True, default='Loading your experience...')),
                ('loading_text', models.CharField(blank=True, max_length=100)),
                ('overlay_color', models.CharField(default='#000000', max_length=20)),
                ('overlay_opacity', models.DecimalField(decimal_places=2, default=0.4, help_text='0=transparent, 1=solid overlay for text readability', max_digits=3)),
                ('overlay_blur_px', models.PositiveSmallIntegerField(blank=True, default=0, help_text='Background blur (0=off, 1-20 for blur)')),
                ('animation_enabled', models.BooleanField(default=True)),
                ('animation_type', models.CharField(choices=[('fade', 'Fade'), ('zoom', 'Zoom'), ('slide', 'Slide from bottom'), ('slide_up', 'Slide up'), ('slide_left', 'Slide from right'), ('none', 'None')], default='fade', max_length=20)),
                ('animation_duration_ms', models.PositiveIntegerField(default=600)),
                ('auto_close_seconds', models.PositiveSmallIntegerField(default=0, help_text='Auto-close after N seconds (0=manual/skip only)')),
                ('loader_type', models.CharField(choices=[('none', 'None'), ('spinner', 'Spinner'), ('progress_bar', 'Progress bar'), ('dots', 'Dots')], default='spinner', max_length=20)),
                ('sound_enabled', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Splash Screen Settings',
                'verbose_name_plural': 'Splash Screen Settings',
            },
        ),
    ]
