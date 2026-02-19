from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('cms', '0001_initial')]

    operations = [
        migrations.AlterField(
            model_name='cmsnotification',
            name='link',
            field=models.CharField(blank=True, help_text='Link path e.g. /admin-login/contact/', max_length=500),
        ),
    ]
