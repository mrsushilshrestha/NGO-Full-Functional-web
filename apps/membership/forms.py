from django import forms
from .models import VolunteerApplication, MembershipApplication, MembershipFee


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['name', 'contact_number', 'email', 'profile_image', 'location',
                  'availability', 'past_experience']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'past_experience': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_profile_image(self):
        img = self.cleaned_data.get('profile_image')
        if img and img.size > 200 * 1024:  # 200 KB
            raise forms.ValidationError('Image size must be 200 KB or less.')
        return img


class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['name', 'email', 'phone', 'member_type', 'payment_method']
