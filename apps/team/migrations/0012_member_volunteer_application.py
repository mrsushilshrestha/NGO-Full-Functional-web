# Migration: Link Member to VolunteerApplication so each approval creates/updates only one Member (no overwriting others)

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('team', '0011_province_district_member_updates'),
        ('membership', '0003_volunteerapplication_cv_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='volunteer_application',
            field=models.OneToOneField(
                blank=True,
                help_text='Set when this Member was created from an approved volunteer application; ensures one Member per application.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='member_record',
                to='membership.volunteerapplication',
            ),
        ),
    ]
