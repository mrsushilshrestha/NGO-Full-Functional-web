# Cards per row and cards per page (Member Card Settings)

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('team', '0013_join_us_settings_and_member_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='teampagesettings',
            name='cards_per_row',
            field=models.PositiveIntegerField(
                choices=[(2, '2'), (3, '3'), (4, '4'), (5, '5')],
                default=3,
                help_text='Number of member cards per row (desktop/tablet). Mobile will show 1–2 per row.',
            ),
        ),
        migrations.AddField(
            model_name='teampagesettings',
            name='cards_per_page',
            field=models.PositiveIntegerField(
                choices=[(6, '6'), (8, '8'), (12, '12'), (18, '18'), (24, '24')],
                default=12,
                help_text='Number of volunteer cards per page (pagination).',
            ),
        ),
    ]
