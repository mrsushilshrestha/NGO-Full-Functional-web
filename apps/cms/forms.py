from django import forms
from apps.core.models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage, NavItem, SiteTheme, SiteIdentity
from apps.about.models import OrganizationInfo, Founder, ChapterLocation, Achievement
from apps.impact.models import ImpactStat
from apps.contact.models import ContactInfo, QuickResponse, ChatSettings
from apps.donation.models import DonationTier, BankDetail
from apps.team.models import Member, Chapter, Collaboration, TeamPageSettings
from apps.programs.models import Program, Category
from apps.cms.models import IconConfig
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


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'member_id': forms.TextInput(attrs={'readonly': True, 'style': 'background-color: #f5f5f5; cursor: not-allowed;'}),
        }
        help_texts = {
            'member_id': 'Auto-generated based on member type. Cannot be edited manually.',
            'member_type': 'Select Board Member or Volunteer. Member ID will be generated automatically.',
        }


class TeamPageSettingsForm(forms.ModelForm):
    clear_watermark = forms.BooleanField(required=False, label='Remove background image (clear to default)')

    class Meta:
        model = TeamPageSettings
        fields = '__all__'
        widgets = {
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
