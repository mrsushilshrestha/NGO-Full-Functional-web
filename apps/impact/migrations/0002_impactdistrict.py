# Generated for Impact District Map

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_id', models.CharField(help_text='Must match SVG path id (e.g. NPBA, NPKA, NPLU).', max_length=20, unique=True)),
                ('display_name', models.CharField(blank=True, help_text='Optional override for legend/tooltip', max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'district_id'],
            },
        ),
    ]
