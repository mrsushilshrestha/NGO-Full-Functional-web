# Generated manually for payment integration
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=200)),
                ('account_name', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=100)),
                ('branch', models.CharField(blank=True, max_length=200)),
                ('swift_code', models.CharField(blank=True, max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='donation',
            name='pidx',
            field=models.CharField(blank=True, help_text='Khalti payment ID', max_length=100),
        ),
        migrations.AddField(
            model_name='donation',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='donation',
            name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('canceled', 'Canceled')],
                default='pending',
                max_length=20,
            ),
        ),
    ]
