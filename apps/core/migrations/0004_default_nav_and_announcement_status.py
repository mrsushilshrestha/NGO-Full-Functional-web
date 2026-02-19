from django.db import migrations


def create_default_nav(apps, schema_editor):
    NavItem = apps.get_model('core', 'NavItem')
    defaults = [
        ('Home', '/', 'fas fa-home', 0, False),
        ('About', '/about/', 'fas fa-info-circle', 1, False),
        ('Programs', '/programs/', 'fas fa-calendar-alt', 2, False),
        ('Team', '/team/', 'fas fa-users', 3, False),
        ('Impact', '/impact/', 'fas fa-chart-line', 4, False),
        ('Contact', '/contact/', 'fas fa-envelope', 5, False),
        ('Donate', '/donate/', 'fas fa-heart', 6, True),
    ]
    for title, url, icon, order, is_btn in defaults:
        NavItem.objects.get_or_create(url=url, defaults={'title': title, 'icon_class': icon, 'order': order, 'is_button': is_btn})


def set_announcements_published(apps, schema_editor):
    AnnouncementPopup = apps.get_model('core', 'AnnouncementPopup')
    AnnouncementPopup.objects.filter(status='draft').update(status='published')


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('core', '0003_nav_theme_announcement_enhancements')]

    operations = [
        migrations.RunPython(create_default_nav, reverse_noop),
        migrations.RunPython(set_announcements_published, reverse_noop),
    ]
