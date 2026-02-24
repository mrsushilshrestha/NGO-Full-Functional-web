from django import forms
from apps.core.models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage, NavItem, SiteTheme, SiteIdentity, SplashScreenSettings
from apps.about.models import OrganizationInfo, Founder, ChapterLocation, Achievement
from apps.impact.models import ImpactStat, ImpactDistrict
from apps.contact.models import ContactInfo, QuickResponse, ChatSettings
from apps.donation.models import DonationTier, BankDetail
from apps.team.models import Member, Chapter, Location, Collaboration, TeamPageSettings
from apps.programs.models import Program, Category
from apps.cms.models import IconConfig, SMSSettings, SMSMessageTemplate, EmailSettings, EmailMessageTemplate
from ckeditor.widgets import CKEditorWidget


class IconConfigForm(forms.ModelForm):
    class Meta:
        model = IconConfig
        fields = '__all__'
        widgets = {
            'icon_class': forms.TextInput(attrs={'placeholder': 'fas fa-home'}),
            'custom_svg': forms.FileInput(attrs={'accept': '.svg'}),
        }

    def clean_custom_svg(self):
        f = self.cleaned_data.get('custom_svg')
        if f and not f.name.lower().endswith('.svg'):
            raise forms.ValidationError('Only SVG files are allowed.')
        return f


class HeroBannerForm(forms.ModelForm):
    class Meta:
        model = HeroBanner
        fields = '__all__'
        widgets = {
            'link_url': forms.URLInput(attrs={'placeholder': 'https://'}),
            'overlay_opacity': forms.NumberInput(attrs={'min': 0, 'max': 1, 'step': 0.05}),
        }


class SplashScreenSettingsForm(forms.ModelForm):
    clear_background_image = forms.BooleanField(required=False, label='Remove background image (use color only)')
    clear_logo = forms.BooleanField(required=False, label='Remove logo')

    class Meta:
        model = SplashScreenSettings
        exclude = ('z_index', 'overlay_blur_px', 'sound_enabled')
        widgets = {
            'background_image': forms.FileInput(attrs={'accept': '.jpg,.jpeg,.png,.webp,.gif', 'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'accept': '.jpg,.jpeg,.png,.webp,.gif,.svg', 'class': 'form-control'}),
            'background_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'style': 'width:60px;height:38px;padding:4px'}),
            'overlay_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color', 'style': 'width:60px;height:38px;padding:4px'}),
            'subtitle_text': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'title_text': forms.TextInput(attrs={'class': 'form-control'}),
            'loading_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Loading...'}),
            'overlay_opacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 1, 'step': 0.1}),
            'animation_type': forms.Select(attrs={'class': 'form-select'}),
            'animation_duration_ms': forms.NumberInput(attrs={'class': 'form-control'}),
            'auto_close_seconds': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0 = click to skip'}),
            'loader_type': forms.Select(attrs={'class': 'form-select'}),
        }


class HomeContentForm(forms.ModelForm):
    class Meta:
        model = HomeContent
        fields = '__all__'
        widgets = {'content': forms.Textarea(attrs={'rows': 5})}


class AnnouncementPopupForm(forms.ModelForm):
    ALLOWED_IMAGE_TYPES = ('image/jpeg', 'image/jpg', 'image/png', 'image/webp')
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

    class Meta:
        model = AnnouncementPopup
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={'accept': '.jpg,.jpeg,.png,.webp'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'link_url': forms.URLInput(attrs={'placeholder': 'https:// or /path/'}),
        }

    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img and hasattr(img, 'content_type'):
            # Only validate new uploads; existing ImageFieldFile has no content_type
            if img.content_type not in self.ALLOWED_IMAGE_TYPES:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
            if img.size > self.MAX_IMAGE_SIZE:
                raise forms.ValidationError('Image must be 5MB or less.')
        return img


class NavItemForm(forms.ModelForm):
    class Meta:
        model = NavItem
        fields = '__all__'
        widgets = {
            'url': forms.TextInput(attrs={'placeholder': '/about/ or https://...'}),
            'icon_class': forms.TextInput(attrs={'placeholder': 'fas fa-home'}),
        }


class SiteThemeForm(forms.ModelForm):
    class Meta:
        model = SiteTheme
        fields = '__all__'
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'nav_bg_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'nav_text_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'dark_mode_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dark_bg_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'dark_text_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'dark_card_bg': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'nav_hover_color': forms.TextInput(attrs={'placeholder': 'rgba(255,255,255,0.15)'}),
            'button_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
            'button_hover_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:60px;height:36px;padding:2px'}),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = '__all__'


class OrganizationInfoForm(forms.ModelForm):
    class Meta:
        model = OrganizationInfo
        fields = '__all__'
        widgets = {
            'mission': CKEditorWidget(),
            'vision': CKEditorWidget(),
            'objectives': CKEditorWidget(),
            'history': CKEditorWidget(),
        }


class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        fields = '__all__'
        widgets = {'bio': CKEditorWidget()}


class ChapterLocationForm(forms.ModelForm):
    class Meta:
        model = ChapterLocation
        fields = '__all__'


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'
        widgets = {'description': CKEditorWidget()}


class ImpactStatForm(forms.ModelForm):
    class Meta:
        model = ImpactStat
        fields = '__all__'
        widgets = {'icon': forms.TextInput(attrs={'placeholder': 'fa-users'})}


# Valid district IDs from Nepal map SVG (np0.svg)
IMPACT_DISTRICT_IDS = [
    ('NPBA', 'Bagmati'), ('NPBH', 'Bheri'), ('NPJA', 'Janakpur'), ('NPKA', 'Karnali'),
    ('NPKO', 'Bhojpur'), ('NPLU', 'Lumbini'), ('NPMA', 'Mahakali'), ('NPME', 'Mechi'),
    ('NPNA', 'Narayani'), ('NPDH', 'Dhawalagiri'), ('NPGA', 'Gandaki'), ('NPRA', 'Rapti'),
    ('NPSA', 'Sagarmatha'), ('NPSE', 'Seti'),
]


class ImpactDistrictForm(forms.ModelForm):
    class Meta:
        model = ImpactDistrict
        fields = '__all__'
        widgets = {
            'district_id': forms.Select(choices=IMPACT_DISTRICT_IDS, attrs={'class': 'form-select'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional override'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        used = ImpactDistrict.objects.values_list('district_id', flat=True)
        self.fields['district_id'].choices = [c for c in IMPACT_DISTRICT_IDS if c[0] not in used or (self.instance and self.instance.district_id == c[0])]
        if not self.fields['district_id'].choices and self.instance:
            self.fields['district_id'].choices = IMPACT_DISTRICT_IDS


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = '__all__'
        widgets = {'map_embed': forms.Textarea(attrs={'rows': 4})}


class DonationTierForm(forms.ModelForm):
    class Meta:
        model = DonationTier
        fields = '__all__'


class BankDetailForm(forms.ModelForm):
    class Meta:
        model = BankDetail
        fields = '__all__'


class SiteIdentityForm(forms.ModelForm):
    class Meta:
        model = SiteIdentity
        fields = '__all__'
        widgets = {
            'favicon': forms.FileInput(attrs={'accept': '.ico,.png,.svg'}),
        }

    def clean_favicon(self):
        f = self.cleaned_data.get('favicon')
        if f:
            ext = f.name.lower().split('.')[-1]
            if ext not in ('ico', 'png', 'svg'):
                raise forms.ValidationError('Favicon must be ICO, PNG, or SVG format.')
        return f


class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'full_description': CKEditorWidget(),
            'objectives': CKEditorWidget(),
            'programs_activities': CKEditorWidget(),
            'impact_outcomes': CKEditorWidget(),
            'agreement_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TeamChapterForm(forms.ModelForm):
    """Team Chapter (board filter) - CMS CRUD."""
    class Meta:
        model = Chapter
        fields = ['name', 'order', 'is_active']


class LocationForm(forms.ModelForm):
    """Location (volunteer filter) - CMS CRUD."""
    class Meta:
        model = Location
        fields = ['name', 'code', 'order', 'is_active']
        help_texts = {'code': 'Unique code used in URLs/filters (e.g. kathmandu). Do not change if members use it.'}


class MemberForm(forms.ModelForm):
    """Member edit form. Location is not shown — volunteer location comes from district (auto-assigned)."""
    class Meta:
        model = Member
        exclude = ['location']  # Volunteer location is derived from district; no manual location selector
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'member_id': forms.TextInput(attrs={'readonly': True, 'style': 'background-color: #f5f5f5; cursor: not-allowed;'}),
        }
        help_texts = {
            'member_id': 'Auto-generated based on member type. Cannot be edited manually.',
            'member_type': 'Select Board Member or Volunteer. Member ID will be generated automatically.',
            'district': 'For volunteers: location is shown from district. Set district here; no separate location field.',
        }


class TeamPageSettingsForm(forms.ModelForm):
    clear_watermark = forms.BooleanField(required=False, label='Remove background image (clear to default)')
    clear_join_us_image = forms.BooleanField(required=False, label='Remove Join Us image')

    class Meta:
        model = TeamPageSettings
        fields = '__all__'
        widgets = {
            'join_us_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Join Our Community'}),
            'join_us_subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short tagline'}),
            'join_us_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional longer description'}),
            'join_us_image': forms.FileInput(attrs={'class': 'form-control'}),
            'title_text': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle_template': forms.TextInput(attrs={'class': 'form-control'}),
            'title_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'subtitle_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'board_line_color': forms.TextInput(attrs={'class': 'form-control'}),
            'board_line_color_2': forms.TextInput(attrs={'class': 'form-control'}),
            'volunteer_line_color': forms.TextInput(attrs={'class': 'form-control'}),
            'volunteer_line_color_2': forms.TextInput(attrs={'class': 'form-control'}),
            'title_font_family': forms.Select(attrs={'class': 'form-select'}),
            'subtitle_font_family': forms.Select(attrs={'class': 'form-select'}),
            'heading_align': forms.Select(attrs={'class': 'form-select'}),
            'title_animation': forms.Select(attrs={'class': 'form-select'}),
            'theme_mode': forms.Select(attrs={'class': 'form-select'}),
            'card_hover_effect': forms.Select(attrs={'class': 'form-select'}),
            'card_shadow': forms.Select(attrs={'class': 'form-select'}),
            'card_animation': forms.Select(attrs={'class': 'form-select'}),
            'board_line_style': forms.Select(attrs={'class': 'form-select'}),
            'volunteer_line_style': forms.Select(attrs={'class': 'form-select'}),
            'watermark_position': forms.Select(attrs={'class': 'form-select'}),
            'title_font_size_px': forms.NumberInput(attrs={'min': 18, 'max': 90, 'class': 'form-control'}),
            'subtitle_font_size_px': forms.NumberInput(attrs={'min': 12, 'max': 40, 'class': 'form-control'}),
            'typing_speed_ms': forms.NumberInput(attrs={'min': 20, 'max': 250, 'class': 'form-control'}),
            'watermark_opacity': forms.NumberInput(attrs={'min': 0, 'max': 1, 'step': 0.01, 'class': 'form-control'}),
            'watermark_size_percent': forms.NumberInput(attrs={'min': 10, 'max': 150, 'class': 'form-control'}),
            'board_line_thickness_px': forms.NumberInput(attrs={'min': 1, 'max': 14, 'class': 'form-control'}),
            'board_line_length_percent': forms.NumberInput(attrs={'min': 10, 'max': 100, 'class': 'form-control'}),
            'volunteer_line_thickness_px': forms.NumberInput(attrs={'min': 1, 'max': 14, 'class': 'form-control'}),
            'volunteer_line_length_percent': forms.NumberInput(attrs={'min': 10, 'max': 100, 'class': 'form-control'}),
            'cards_per_row': forms.Select(attrs={'class': 'form-select'}),
            'cards_per_page': forms.Select(attrs={'class': 'form-select'}),
            'card_radius_px': forms.NumberInput(attrs={'min': 8, 'max': 40, 'class': 'form-control'}),
            'card_min_height_px': forms.NumberInput(attrs={'min': 240, 'max': 800, 'class': 'form-control'}),
            'card_max_height_px': forms.NumberInput(attrs={'min': 240, 'max': 900, 'class': 'form-control'}),
            'social_icon_size_px': forms.NumberInput(attrs={'min': 20, 'max': 48, 'class': 'form-control'}),
            'name_font_size_px': forms.NumberInput(attrs={'min': 14, 'max': 38, 'class': 'form-control'}),
            'role_font_size_px': forms.NumberInput(attrs={'min': 10, 'max': 24, 'class': 'form-control'}),
            'id_font_size_px': forms.NumberInput(attrs={'min': 9, 'max': 20, 'class': 'form-control'}),
            'section_spacing_px': forms.NumberInput(attrs={'min': 8, 'max': 64, 'class': 'form-control'}),
            'card_padding_px': forms.NumberInput(attrs={'min': 8, 'max': 48, 'class': 'form-control'}),
            'background_watermark': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'description': CKEditorWidget(),
        }


class QuickResponseForm(forms.ModelForm):
    class Meta:
        model = QuickResponse
        # Old version: simple quick responses (no keywords UI)
        fields = ['message', 'order', 'is_active']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }


class ChatSettingsForm(forms.ModelForm):
    class Meta:
        model = ChatSettings
        # Old version: basic built-in chat settings only
        fields = ['is_enabled', 'auto_response_enabled', 'auto_response_message']
        widgets = {
            'auto_response_message': forms.Textarea(attrs={'rows': 3}),
        }


# --- SMS Configuration Forms (for application workflow notifications) ---
class SMSSettingsForm(forms.ModelForm):
    """CMS form for SMS gateway configuration. User-friendly for non-technical staff."""
    class Meta:
        model = SMSSettings
        fields = [
            'sms_enabled', 'sender_email', 'sender_id',
            'api_key', 'api_secret', 'endpoint_url',
        ]
        widgets = {
            'sender_email': forms.EmailInput(attrs={
                'placeholder': 'notifications@xyz.org',
                'class': 'form-control',
            }),
            'sender_id': forms.TextInput(attrs={
                'placeholder': 'NHAF',
                'class': 'form-control',
            }),
            'api_key': forms.TextInput(attrs={
                'placeholder': 'Your API key',
                'class': 'form-control',
            }),
            'api_secret': forms.TextInput(attrs={
                'placeholder': 'Optional',
                'class': 'form-control',
            }),
            'endpoint_url': forms.URLInput(attrs={
                'placeholder': 'https://api.example.com/sms',
                'class': 'form-control',
            }),
        }
        labels = {
            'sms_enabled': 'Enable SMS notifications',
            'sender_email': 'Sender email address',
            'sender_id': 'Sender ID',
            'api_key': 'API Key',
            'api_secret': 'API Secret',
            'endpoint_url': 'API Endpoint URL',
        }
        help_texts = {
            'sms_enabled': 'Turn on to send SMS at form submission, approval, and rejection.',
            'sender_email': 'Email used for email-to-SMS gateways. Example: notifications@xyz.org',
            'sender_id': 'Text shown as sender on recipient phone (provider-dependent)',
            'api_key': 'Your SMS gateway API key from the provider dashboard',
            'api_secret': 'API secret if your provider requires it',
            'endpoint_url': 'Optional. API URL for sending SMS (some providers use fixed URLs)',
        }


class SMSMessageTemplateForm(forms.ModelForm):
    """CMS form for editing SMS message templates with placeholder support."""
    class Meta:
        model = SMSMessageTemplate
        fields = ['template_type', 'subject', 'message', 'is_active']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional subject'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'template_type': 'Template type',
            'subject': 'Subject (optional)',
            'message': 'Message content',
            'is_active': 'Active',
        }
        help_texts = {
            'message': 'Use placeholders: {name}, {application_type}, {date}',
        }


class EmailSettingsForm(forms.ModelForm):
    class Meta:
        model = EmailSettings
        fields = [
            'email_enabled', 'sender_email', 'sender_name',
            'smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_username', 'smtp_password',
            'organization_name', 'contact_info',
        ]
        widgets = {
            'sender_email': forms.EmailInput(attrs={'placeholder': 'notifications@xyz.org', 'class': 'form-control'}),
            'sender_name': forms.TextInput(attrs={'placeholder': 'NHAF Nepal', 'class': 'form-control'}),
            'smtp_host': forms.TextInput(attrs={'placeholder': 'smtp.gmail.com', 'class': 'form-control'}),
            'smtp_port': forms.NumberInput(attrs={'placeholder': '587', 'class': 'form-control', 'min': 1, 'max': 65535}),
            'smtp_username': forms.TextInput(attrs={'placeholder': 'your@email.com', 'class': 'form-control'}),
            'smtp_password': forms.PasswordInput(attrs={'placeholder': 'App password', 'class': 'form-control', 'autocomplete': 'new-password'}),
            'organization_name': forms.TextInput(attrs={'placeholder': 'NHAF Nepal', 'class': 'form-control'}),
            'contact_info': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Phone, address, or website', 'class': 'form-control'}),
        }
        help_texts = {
            'sender_email': 'Required for sending. If empty, no emails are sent.',
            'smtp_host': 'Leave blank to use server default. Set for custom SMTP (e.g. Gmail, SendGrid).',
            'smtp_password': 'App password for Gmail; or your SMTP password.',
            'organization_name': 'Used in templates as {organization_name}.',
            'contact_info': 'Optional footer text. Used in templates as {contact_info}.',
        }


class EmailMessageTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailMessageTemplate
        fields = ['template_type', 'subject', 'body', 'footer', 'is_active']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Application Received'}),
            'body': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'placeholder': 'Dear {name},\n\n[Your message here]\n\nThank you,\n{organization_name}'}),
            'footer': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Optional: Thank you,\n{organization_name}\n{contact_info}'}),
        }
        help_texts = {
            'body': 'Placeholders: {name}, {application_type}, {date}, {organization_name}',
            'footer': 'Optional. Appended after the body. Placeholders: {organization_name}, {contact_info}',
        }
