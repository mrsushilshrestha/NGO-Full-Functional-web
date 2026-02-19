from django.db import migrations


def create_default_icons(apps, schema_editor):
    IconConfig = apps.get_model('cms', 'IconConfig')
    defaults = [
        ('nav_home', 'fas fa-home'),
        ('nav_about', 'fas fa-info-circle'),
        ('nav_programs', 'fas fa-calendar-alt'),
        ('nav_team', 'fas fa-users'),
        ('nav_impact', 'fas fa-chart-line'),
        ('nav_contact', 'fas fa-envelope'),
        ('nav_donate', 'fas fa-heart'),
    ]
    for loc, iclass in defaults:
        IconConfig.objects.get_or_create(location=loc, defaults={'icon_class': iclass})


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('cms', '0002_notification_link_charfield')]

    operations = [
        migrations.RunPython(create_default_icons, reverse_noop),
    ]
