from django import forms
from apps.core.models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage, NavItem, SiteTheme, SiteIdentity
from apps.about.models import OrganizationInfo, Founder, ChapterLocation, Achievement
from apps.impact.models import ImpactStat
from apps.contact.models import ContactInfo, QuickResponse, ChatSettings
from apps.donation.models import DonationTier, BankDetail
from apps.team.models import Member, Chapter, Collaboration
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
