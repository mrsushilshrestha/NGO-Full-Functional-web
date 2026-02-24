from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_swipe_autosearch_tag_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpagesettings',
            name='show_title',
            field=models.BooleanField(default=True, help_text='Show or hide the main blog page title'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_title_color',
            field=models.CharField(blank=True, default='#111827', help_text='CSS color for post titles', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_content_color',
            field=models.CharField(blank=True, default='#4b5563', help_text='CSS color for post content/body', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_title_font_size_px',
            field=models.PositiveIntegerField(default=20, help_text='Title font size in pixels'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_body_font_size_px',
            field=models.PositiveIntegerField(default=15, help_text='Body font size in pixels'),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_title_font_family',
            field=models.CharField(blank=True, default="'Playfair Display', Georgia, serif", help_text='CSS font-family for titles', max_length=100),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='post_body_font_family',
            field=models.CharField(blank=True, default="'Inter', system-ui, sans-serif", help_text='CSS font-family for body text', max_length=100),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='card_bg_color',
            field=models.CharField(blank=True, default='#fdfdfd', help_text='Background color for blog cards', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='card_border_color',
            field=models.CharField(blank=True, default='rgba(0,0,0,0.06)', help_text='Border color for blog cards', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='card_shadow_style',
            field=models.CharField(choices=[('none', 'None'), ('light', 'Light'), ('medium', 'Medium')], default='light', help_text='Shadow intensity for blog cards', max_length=10),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='primary_color',
            field=models.CharField(blank=True, default='#0B5345', help_text='Primary theme color for blog', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='secondary_color',
            field=models.CharField(blank=True, default='#148f77', help_text='Secondary theme color for blog', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='link_color',
            field=models.CharField(blank=True, default='#0B5345', help_text='Default link color in blog content', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='button_color',
            field=models.CharField(blank=True, default='#0B5345', help_text='Primary button color in blog', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='global_card_bg_color',
            field=models.CharField(blank=True, default='#f9fafb', help_text='Background color for generic blog panels', max_length=20),
        ),
        migrations.AddField(
            model_name='blogpagesettings',
            name='text_align',
            field=models.CharField(choices=[('left', 'Left'), ('center', 'Center'), ('justify', 'Justify')], default='left', help_text='Default text alignment for blog paragraphs', max_length=10),
        ),
    ]

