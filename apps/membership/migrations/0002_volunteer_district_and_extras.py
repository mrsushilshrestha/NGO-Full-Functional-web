# Migration: VolunteerApplication - district FK, extra fields; location/availability optional

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0001_initial'),
        ('team', '0011_province_district_member_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerapplication',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='volunteer_applications', to='team.district'),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='volunteering_interest',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='municipality',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='ward',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='volunteerapplication',
            name='area',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='volunteerapplication',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='volunteerapplication',
            name='availability',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
