# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('core', '0002_herobanner_display_options_and_announcement_image')]

    operations = [
        migrations.CreateModel(
            name='NavItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(help_text='URL path e.g. /about/ or https://...', max_length=500)),
                ('icon_class', models.CharField(blank=True, help_text='Font Awesome e.g. fas fa-home', max_length=100)),
                ('custom_icon', models.FileField(blank=True, null=True, upload_to='nav_icons/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_button', models.BooleanField(default=False, help_text='Style as button (e.g. Donate)')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.navitem')),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='SiteTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_color', models.CharField(default='#0B5345', max_length=7)),
                ('secondary_color', models.CharField(default='#148f77', max_length=7)),
                ('nav_bg_color', models.CharField(default='#0B5345', max_length=7)),
                ('nav_text_color', models.CharField(default='#ffffff', max_length=7)),
                ('nav_hover_color', models.CharField(default='rgba(255,255,255,0.15)', max_length=30)),
                ('button_color', models.CharField(default='#c17f59', max_length=7)),
                ('button_hover_color', models.CharField(default='#a86d4a', max_length=7)),
            ],
            options={'verbose_name': 'Site theme', 'verbose_name_plural': 'Site theme'},
        ),
        migrations.AlterField(
            model_name='announcementpopup',
            name='link_url',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='announcementpopup',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='announcementpopup',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published'), ('expired', 'Expired')], default='draft', max_length=20),
        ),
        migrations.AlterModelOptions(
            name='announcementpopup',
            options={'ordering': ['-start_date', '-id']},
        ),
    ]
