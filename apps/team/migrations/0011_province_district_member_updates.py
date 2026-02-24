# Migration: Province, District models; Member.district, Member.exclude_from_public

from django.db import migrations, models
import django.db.models.deletion


def create_nepal_provinces_districts(apps, schema_editor):
    """Seed Nepal provinces and districts for database-driven dropdown."""
    Province = apps.get_model('team', 'Province')
    District = apps.get_model('team', 'District')
    provinces_data = [
        (1, 'Koshi', ['Bhojpur', 'Dhankuta', 'Ilam', 'Jhapa', 'Khotang', 'Morang', 'Okhaldhunga', 'Panchthar', 'Sankhuwasabha', 'Solukhumbu', 'Sunsari', 'Taplejung', 'Terhathum', 'Udayapur']),
        (2, 'Madhesh', ['Bara', 'Dhanusha', 'Mahottari', 'Parsa', 'Rautahat', 'Saptari', 'Sarlahi', 'Siraha']),
        (3, 'Bagmati', ['Bhaktapur', 'Chitwan', 'Dhading', 'Dolakha', 'Kathmandu', 'Kavrepalanchok', 'Lalitpur', 'Makwanpur', 'Nuwakot', 'Ramechhap', 'Rasuwa', 'Sindhuli', 'Sindhupalchok']),
        (4, 'Gandaki', ['Baglung', 'Gorkha', 'Kaski', 'Lamjung', 'Manang', 'Mustang', 'Myagdi', 'Nawalpur', 'Parbat', 'Syangja', 'Tanahu']),
        (5, 'Lumbini', ['Arghakhanchi', 'Banke', 'Bardia', 'Dang', 'Gulmi', 'Kapilvastu', 'Parasi', 'Palpa', 'Pyuthan', 'Rolpa', 'Rukum East', 'Rupandehi']),
        (6, 'Karnali', ['Dailekh', 'Dolpa', 'Humla', 'Jajarkot', 'Jumla', 'Kalikot', 'Mugu', 'Rukum West', 'Salyan', 'Surkhet']),
        (7, 'Sudurpashchim', ['Achham', 'Baitadi', 'Bajhang', 'Bajura', 'Dadeldhura', 'Darchula', 'Doti', 'Kailali', 'Kanchanpur']),
    ]
    for order, pname, districts in provinces_data:
        prov, _ = Province.objects.get_or_create(name=pname, defaults={'order': order})
        for i, dname in enumerate(districts):
            code = dname.lower().replace(' ', '_').replace('-', '')
            District.objects.get_or_create(
                province=prov, code=code,
                defaults={'name': dname, 'order': i}
            )


def reverse_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('team', '0010_add_location_and_chapter_fields')]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(help_text='Unique code (e.g. kathmandu)', max_length=50, unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='team.province')),
            ],
            options={'ordering': ['province', 'order', 'name']},
        ),
        migrations.AddField(
            model_name='member',
            name='district',
            field=models.ForeignKey(blank=True, help_text='District for filtering volunteers', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='team.district'),
        ),
        migrations.AddField(
            model_name='member',
            name='exclude_from_public',
            field=models.BooleanField(default=False, help_text='Hide from public site (e.g. members from paid membership with bank info)'),
        ),
        migrations.RunPython(create_nepal_provinces_districts, reverse_noop),
    ]
