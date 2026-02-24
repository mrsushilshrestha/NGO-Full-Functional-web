"""Blog forms for CMS."""
from django import forms
from django.utils.text import slugify
from django.forms import inlineformset_factory
from .models import BlogPost, BlogAuthor, BlogCategory, BlogTag, BlogPageSettings, BlogContentBlock


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        # slug optional on add - auto-generated from title if empty
        fields = [
            'title', 'slug', 'date', 'status', 'featured',
            'author', 'author_name', 'author_role', 'author_avatar',
            'category', 'tags', 'excerpt', 'long_excerpt',
            'featured_image', 'image_caption',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'url-slug'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Override author name'}),
            'author_role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Override author role'}),
            'author_avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short excerpt for cards'}),
            'long_excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Long intro for detail page'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_caption': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image caption'}),
        }
        help_texts = {'slug': 'Leave blank to auto-generate from title.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        if not slug and self.cleaned_data.get('title'):
            slug = slugify(self.cleaned_data['title'])[:300] or 'post'
        return slug


class BlogContentBlockForm(forms.ModelForm):
    class Meta:
        model = BlogContentBlock
        fields = ['block_type', 'content', 'attribution', 'order']
        widgets = {
            'block_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'attribution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'For quotes: attribution'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


BlogContentBlockFormSet = inlineformset_factory(
    BlogPost, BlogContentBlock, form=BlogContentBlockForm,
    extra=2, can_delete=True, can_order=False
)


class BlogAuthorForm(forms.ModelForm):
    class Meta:
        model = BlogAuthor
        fields = ['name', 'role', 'avatar', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Health Officer'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ['name', 'slug', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-from-name'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class BlogTagForm(forms.ModelForm):
    class Meta:
        model = BlogTag
        fields = ['name', 'slug', 'order', 'is_popular']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'auto-from-name'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_popular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BlogPageSettingsForm(forms.ModelForm):
    clear_banner = forms.BooleanField(required=False, label='Remove banner image')

    class Meta:
        model = BlogPageSettings
        fields = [
            'hero_title', 'hero_subtitle', 'banner_image',
            'posts_per_page', 'enable_featured_layout', 'default_sort',
            'seo_title', 'seo_description',
            'enable_swipe_effect', 'enable_auto_search',
            'show_title',
            'post_title_color', 'post_content_color',
            'post_title_font_size_px', 'post_body_font_size_px',
            'post_title_font_family', 'post_body_font_family',
            'card_bg_color', 'card_border_color', 'card_shadow_style',
            'primary_color', 'secondary_color',
            'link_color', 'button_color',
            'global_card_bg_color', 'text_align',
        ]
        widgets = {
            'hero_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control'}),
            'posts_per_page': forms.NumberInput(attrs={'class': 'form-control', 'min': 3, 'max': 50}),
            'enable_featured_layout': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'default_sort': forms.Select(attrs={'class': 'form-select'}),
            'seo_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SEO title'}),
            'seo_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'SEO description'}),
            'enable_swipe_effect': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enable_auto_search': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_title': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'post_title_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'post_content_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'post_title_font_size_px': forms.NumberInput(attrs={'class': 'form-control', 'min': 12, 'max': 48}),
            'post_body_font_size_px': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 32}),
            'post_title_font_family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. \"Playfair Display\", Georgia, serif'}),
            'post_body_font_family': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. \"Inter\", system-ui, sans-serif'}),
            'card_bg_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'card_border_color': forms.TextInput(attrs={'class': 'form-control'}),
            'card_shadow_style': forms.Select(attrs={'class': 'form-select'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'link_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'button_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'global_card_bg_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'text_align': forms.Select(attrs={'class': 'form-select'}),
        }
