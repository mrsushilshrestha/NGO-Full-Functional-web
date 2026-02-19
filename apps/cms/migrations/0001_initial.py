from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CMSNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('member_pending', 'Member Pending'), ('member_approved', 'Member Approved'), ('member_rejected', 'Member Rejected'), ('payment_received', 'Payment Received'), ('contact_message', 'Contact Message'), ('volunteer_pending', 'Volunteer Pending'), ('system', 'System Alert')], max_length=30)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='IconConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('nav_home', 'Nav: Home'), ('nav_about', 'Nav: About'), ('nav_programs', 'Nav: Programs'), ('nav_team', 'Nav: Team'), ('nav_impact', 'Nav: Impact'), ('nav_contact', 'Nav: Contact'), ('nav_donate', 'Nav: Donate')], max_length=50, unique=True)),
                ('icon_class', models.CharField(default='fas fa-circle', help_text='Font Awesome class e.g. fas fa-home', max_length=100)),
                ('custom_svg', models.FileField(blank=True, null=True, upload_to='icons/')),
            ],
        ),
    ]
