from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('contact', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(db_index=True, help_text='Unique session identifier for user', max_length=100)),
                ('sender_type', models.CharField(choices=[('user', 'User'), ('admin', 'Admin')], max_length=10)),
                ('sender_name', models.CharField(blank=True, max_length=200)),
                ('sender_email', models.EmailField(blank=True, max_length=254)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='QuickResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Quick response text')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['order', 'id']},
        ),
        migrations.CreateModel(
            name='ChatSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=True)),
                ('auto_response_enabled', models.BooleanField(default=False)),
                ('auto_response_message', models.TextField(default='Thank you for contacting us. Our team will respond shortly.')),
            ],
            options={'verbose_name': 'Chat settings', 'verbose_name_plural': 'Chat settings'},
        ),
    ]
