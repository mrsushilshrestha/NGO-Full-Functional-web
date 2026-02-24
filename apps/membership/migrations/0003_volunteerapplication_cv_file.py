# Migration: VolunteerApplication - CV/resume file upload

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('membership', '0002_volunteer_district_and_extras'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerapplication',
            name='cv_file',
            field=models.FileField(blank=True, help_text='CV/Resume (PDF or DOC, max 5MB)', null=True, upload_to='volunteers/cv/'),
        ),
    ]
