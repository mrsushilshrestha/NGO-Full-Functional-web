# Generated for location-based filtering (public) and category (admin)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_team_page_settings_enhanced'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='category',
            field=models.CharField(blank=True, help_text='Internal/admin: category for organization', max_length=100),
        ),
        migrations.AddField(
            model_name='member',
            name='location',
            field=models.CharField(
                blank=True,
                choices=[('', 'Not set'), ('kathmandu', 'Kathmandu'), ('nepalgunj', 'Nepalgunj'), ('pokhara', 'Pokhara'), ('dharan', 'Dharan'), ('other', 'Other')],
                help_text='Public location for filtering (e.g. Kathmandu, Nepalgunj)',
                max_length=50,
            ),
        ),
    ]
