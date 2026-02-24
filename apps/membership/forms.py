from django import forms
from .models import VolunteerApplication, MembershipApplication, MembershipFee


VOLUNTEERING_INTEREST_CHOICES = [
    ('', '-- Please select an area --'),
    ('education', 'Education & Teaching'),
    ('health', 'Health & Medical Support'),
    ('environment', 'Environment & Sanitation'),
    ('disaster', 'Disaster Relief & Management'),
    ('admin', 'Administrative & Data Entry'),
    ('social_media', 'Social Media & Marketing'),
    ('community', 'Community Development'),
    ('events', 'Event Coordination'),
]


# CV: allowed extensions and max size (5MB)
CV_ALLOWED_EXTENSIONS = ('.pdf', '.doc', '.docx')
CV_MAX_SIZE = 5 * 1024 * 1024  # 5 MB


class VolunteerApplicationForm(forms.ModelForm):
    """Volunteer form with district from database. District required. CV optional."""
    class Meta:
        model = VolunteerApplication
        fields = [
            'name', 'contact_number', 'email', 'profile_image', 'cv_file', 'district',
            'municipality', 'ward', 'area', 'volunteering_interest',
            'past_experience', 'availability',
            'facebook_url', 'linkedin_url', 'twitter_url', 'instagram_url',
        ]
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'cv_file': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
            'past_experience': forms.Textarea(attrs={'rows': 4}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/... or https://x.com/...'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.team.models import District
        self.fields['district'].queryset = District.objects.filter(is_active=True).select_related('province').order_by('province__order', 'name')
        self.fields['district'].required = True
        self.fields['volunteering_interest'].widget = forms.Select(attrs={'class': 'form-control'}, choices=VOLUNTEERING_INTEREST_CHOICES)

    def clean_profile_image(self):
        img = self.cleaned_data.get('profile_image')
        if img and img.size > 200 * 1024:  # 200 KB
            raise forms.ValidationError('Profile image must be 200 KB or less.')
        return img

    def clean_cv_file(self):
        f = self.cleaned_data.get('cv_file')
        if not f:
            return f
        ext = None
        if hasattr(f, 'name') and f.name:
            ext = '.' + f.name.rsplit('.', 1)[-1].lower() if '.' in f.name else None
        if ext and ext not in CV_ALLOWED_EXTENSIONS:
            raise forms.ValidationError('CV must be PDF or DOC/DOCX.')
        if f.size > CV_MAX_SIZE:
            raise forms.ValidationError('CV file must be 5 MB or less.')
        return f


class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['name', 'email', 'phone', 'member_type', 'payment_method']
