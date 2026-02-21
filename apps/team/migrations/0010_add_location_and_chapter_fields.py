# Chapter: order, is_active; new Location model; populate Location from choices

from django.db import migrations, models


def populate_locations(apps, schema_editor):
    Location = apps.get_model('team', 'Location')
    data = [
        ('kathmandu', 'Kathmandu', 0),
        ('nepalgunj', 'Nepalgunj', 1),
        ('pokhara', 'Pokhara', 2),
        ('dharan', 'Dharan', 3),
        ('other', 'Other', 4),
    ]
    for code, name, order in data:
        Location.objects.get_or_create(code=code, defaults={'name': name, 'order': order, 'is_active': True})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0009_member_location_and_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chapter',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(help_text='Internal code (e.g. kathmandu)', max_length=50, unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.RunPython(populate_locations, noop),
    ]
