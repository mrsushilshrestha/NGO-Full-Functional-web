from django.db import models
from django.db.models import Q
from django.urls import reverse


class Chapter(models.Model):
    """Chapter/Location for team members"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Member(models.Model):
    """Team member directory"""
    MEMBER_TYPE_CHOICES = [
        ('board', 'Board Member'),
        ('volunteer', 'Volunteer'),
    ]
    name = models.CharField(max_length=200)
    member_id = models.CharField(max_length=50, blank=True, editable=False, help_text='Auto-generated based on member type')
    role = models.CharField(max_length=200, blank=True, help_text='Optional: Specific role or position')
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default='volunteer', help_text='Select Board Member or Volunteer')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    education = models.CharField(max_length=255, blank=True)
    join_year = models.PositiveIntegerField(blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    # Social media links
    facebook_url = models.URLField(blank=True, help_text='Facebook profile URL')
    instagram_url = models.URLField(blank=True, help_text='Instagram profile URL')
    linkedin_url = models.URLField(blank=True, help_text='LinkedIn profile URL')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_member_detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        parts = (self.name or '').split()
        if not parts:
            return ''
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[1][0]).upper()

    def generate_member_id(self):
        """Auto-generate member ID based on member type: NHAFN-B-XXX-YYYY (Board) or NHAFN-M-XXX-YYYY (Volunteer)"""
        from django.utils import timezone
        current_year = self.join_year if self.join_year else timezone.now().year
        
        # Determine prefix based on member_type
        if self.member_type == 'board':
            prefix = 'B'  # Board Member
        else:
            prefix = 'M'  # Volunteer
        
        # Get all members of the same type, ordered by order field then pk (same as list display order)
        same_type_members = Member.objects.filter(
            member_type=self.member_type
        ).order_by('order', 'pk')
        
        # Count how many members of this type exist (including this one)
        # This gives us the position in the list
        total_count = same_type_members.count()
        
        # If this member already exists in DB, find its position
        if self.pk:
            # Get all members before this one in the ordered list
            position = same_type_members.filter(
                Q(order__lt=self.order) | 
                (Q(order=self.order) & Q(pk__lt=self.pk))
            ).count() + 1
        else:
            # New member - position is total count + 1
            position = total_count + 1
        
        return f'NHAFN-{prefix}-{position:03d}-{current_year}'

    def save(self, *args, **kwargs):
        # Auto-generate member_id if not set or empty, or if member_type changed
        if self.pk:
            # Check if member_type changed by comparing with existing instance
            try:
                old_instance = Member.objects.get(pk=self.pk)
                if old_instance.member_type != self.member_type:
                    # Member type changed - regenerate ID
                    self.member_id = self.generate_member_id()
                elif not self.member_id or self.member_id.strip() == '':
                    # ID is missing - generate it
                    self.member_id = self.generate_member_id()
            except Member.DoesNotExist:
                # New instance
                if not self.member_id or self.member_id.strip() == '':
                    self.member_id = self.generate_member_id()
        else:
            # New member - generate ID
            if not self.member_id or self.member_id.strip() == '':
                self.member_id = self.generate_member_id()
        super().save(*args, **kwargs)


class TeamPageSettings(models.Model):
    """Singleton settings to control Team page UI from CMS."""

    ALIGN_CHOICES = [
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ]

    FONT_CHOICES = [
        ('nunito', 'Nunito (friendly)'),
        ('dm_sans', 'DM Sans (default)'),
        ('plus_jakarta', 'Plus Jakarta Sans (modern)'),
        ('inter', 'Inter (clean)'),
        ('poppins', 'Poppins (rounded)'),
        ('open_sans', 'Open Sans (readable)'),
        ('lato', 'Lato (neutral)'),
        ('roboto', 'Roboto (system-like)'),
        ('playfair', 'Playfair Display (serif)'),
        ('merriweather', 'Merriweather (serif)'),
    ]

    TITLE_ANIMATION_CHOICES = [
        ('none', 'None'),
        ('typing', 'Typing'),
        ('fade', 'Fade in'),
        ('slide', 'Slide up'),
        ('zoom', 'Zoom in'),
        ('bounce', 'Bounce'),
    ]

    THEME_MODE_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]

    CARD_HOVER_CHOICES = [
        ('none', 'None'),
        ('lift', 'Lift up'),
        ('scale', 'Scale up'),
        ('glow', 'Glow'),
    ]

    CARD_SHADOW_CHOICES = [
        ('none', 'None'),
        ('soft', 'Soft'),
        ('medium', 'Medium'),
        ('strong', 'Strong'),
    ]

    CARD_ANIMATION_CHOICES = [
        ('none', 'None'),
        ('fadeIn', 'Fade in'),
        ('slideUp', 'Slide up'),
        ('zoomIn', 'Zoom in'),
    ]

    LINE_STYLE_CHOICES = [
        ('solid', 'Solid'),
        ('dashed', 'Dashed'),
        ('gradient', 'Gradient'),
    ]

    WATERMARK_POSITION_CHOICES = [
        ('center', 'Center'),
        ('top-left', 'Top left'),
        ('top-right', 'Top right'),
        ('bottom-left', 'Bottom left'),
        ('bottom-right', 'Bottom right'),
    ]

    # Top heading content
    title_text = models.CharField(max_length=200, default='Our Team')
    subtitle_template = models.CharField(
        max_length=300,
        default='Meet the people behind NHAF Nepal. {count} members dedicated to community health.',
        help_text='Use {count} where the member count should appear.',
    )

    title_font_family = models.CharField(max_length=30, choices=FONT_CHOICES, default='nunito')
    subtitle_font_family = models.CharField(max_length=30, choices=FONT_CHOICES, default='nunito')
    title_font_size_px = models.PositiveIntegerField(default=44, help_text='Title font size in pixels (desktop).')
    subtitle_font_size_px = models.PositiveIntegerField(default=20, help_text='Subtitle font size in pixels (desktop).')
    title_color = models.CharField(max_length=50, default='var(--text-dark)')
    subtitle_color = models.CharField(max_length=50, default='var(--text-muted)')
    heading_align = models.CharField(max_length=10, choices=ALIGN_CHOICES, default='left')

    title_animation = models.CharField(
        max_length=20, choices=TITLE_ANIMATION_CHOICES, default='typing',
        help_text='Animation type for title/subtitle.',
    )
    typing_enabled = models.BooleanField(default=True, help_text='Enable typing animation for title/subtitle (used when animation is Typing).')
    typing_speed_ms = models.PositiveIntegerField(default=90, help_text='Typing speed per character in ms.')

    # Category decorative lines (Board / Volunteer)
    board_line_style = models.CharField(max_length=20, choices=LINE_STYLE_CHOICES, default='gradient')
    board_line_thickness_px = models.PositiveIntegerField(default=4)
    board_line_color = models.CharField(max_length=20, default='var(--primary)')
    board_line_color_2 = models.CharField(max_length=20, default='var(--primary-light)')
    board_line_full_width = models.BooleanField(default=True)
    board_line_length_percent = models.PositiveIntegerField(default=100, help_text='Used when full width is off (10–100).')

    volunteer_line_style = models.CharField(max_length=20, choices=LINE_STYLE_CHOICES, default='gradient')
    volunteer_line_thickness_px = models.PositiveIntegerField(default=4)
    volunteer_line_color = models.CharField(max_length=20, default='var(--primary)')
    volunteer_line_color_2 = models.CharField(max_length=20, default='var(--primary-light)')
    volunteer_line_full_width = models.BooleanField(default=True)
    volunteer_line_length_percent = models.PositiveIntegerField(default=100, help_text='Used when full width is off (10–100).')

    # Search box
    show_search = models.BooleanField(default=True, help_text='Show the search box on the Team page.')

    # Background watermark
    background_watermark = models.ImageField(upload_to='team/backgrounds/', blank=True, null=True)
    watermark_opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.08, help_text='0.00–1.00')
    watermark_position = models.CharField(max_length=20, choices=WATERMARK_POSITION_CHOICES, default='center')
    watermark_size_percent = models.PositiveIntegerField(default=55, help_text='Watermark size as % (10–120).')

    # Member card styling (core knobs)
    card_radius_px = models.PositiveIntegerField(default=18)
    card_min_height_px = models.PositiveIntegerField(default=420)
    card_max_height_px = models.PositiveIntegerField(default=540)
    card_padding_px = models.PositiveIntegerField(default=16, help_text='Card inner padding (px).')
    social_icon_size_px = models.PositiveIntegerField(default=32)
    name_font_size_px = models.PositiveIntegerField(default=22)
    role_font_size_px = models.PositiveIntegerField(default=14)
    id_font_size_px = models.PositiveIntegerField(default=12)
    card_hover_effect = models.CharField(max_length=20, choices=CARD_HOVER_CHOICES, default='lift')
    card_shadow = models.CharField(max_length=20, choices=CARD_SHADOW_CHOICES, default='medium')
    card_animation = models.CharField(max_length=20, choices=CARD_ANIMATION_CHOICES, default='none')
    section_spacing_px = models.PositiveIntegerField(default=24, help_text='Spacing between sections (px).')

    # Team page theme (light/dark)
    theme_mode = models.CharField(max_length=10, choices=THEME_MODE_CHOICES, default='light')

    class Meta:
        verbose_name = 'Team page settings'
        verbose_name_plural = 'Team page settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def get_defaults(cls):
        """Return a dict of default field values for reset-to-default actions."""
        return {
            'title_text': 'Our Team',
            'subtitle_template': 'Meet the people behind NHAF Nepal. {count} members dedicated to community health.',
            'title_font_family': 'nunito',
            'subtitle_font_family': 'nunito',
            'title_font_size_px': 44,
            'subtitle_font_size_px': 20,
            'title_color': 'var(--text-dark)',
            'subtitle_color': 'var(--text-muted)',
            'heading_align': 'left',
            'title_animation': 'typing',
            'typing_enabled': True,
            'typing_speed_ms': 90,
            'board_line_style': 'gradient',
            'board_line_thickness_px': 4,
            'board_line_color': 'var(--primary)',
            'board_line_color_2': 'var(--primary-light)',
            'board_line_full_width': True,
            'board_line_length_percent': 100,
            'volunteer_line_style': 'gradient',
            'volunteer_line_thickness_px': 4,
            'volunteer_line_color': 'var(--primary)',
            'volunteer_line_color_2': 'var(--primary-light)',
            'volunteer_line_full_width': True,
            'volunteer_line_length_percent': 100,
            'show_search': True,
            'watermark_opacity': 0.08,
            'watermark_position': 'center',
            'watermark_size_percent': 55,
            'card_radius_px': 18,
            'card_min_height_px': 420,
            'card_max_height_px': 540,
            'card_padding_px': 16,
            'social_icon_size_px': 32,
            'name_font_size_px': 22,
            'role_font_size_px': 14,
            'id_font_size_px': 12,
            'card_hover_effect': 'lift',
            'card_shadow': 'medium',
            'card_animation': 'none',
            'section_spacing_px': 24,
            'theme_mode': 'light',
        }


class Collaboration(models.Model):
    """Collaboration / Partner Wings - MOUs, partnerships, affiliations"""
    PARTNERSHIP_TYPE_CHOICES = [
        ('mou', 'Memorandum of Understanding (MOU)'),
        ('academic', 'Academic Partner'),
        ('ngo', 'NGO Partner'),
        ('corporate', 'Corporate Partner'),
        ('government', 'Government Partner'),
        ('wing', 'Partner Wing'),
        ('strategic', 'Strategic Partner'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    BACKGROUND_COLOR_CHOICES = [
        ('', 'Default (Warm cream)'),
        ('#faf8f5', 'Cream'),
        ('#f5f2ed', 'Warm beige'),
        ('#f0f7f4', 'Mint green'),
        ('#e8f4f8', 'Soft blue'),
        ('#f8f4e8', 'Light gold'),
        ('#f5f0e8', 'Sand'),
        ('#eef5f0', 'Sage'),
    ]
    organization_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='collaborations/', blank=True, null=True)
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES, default='mou')
    short_description = models.TextField(max_length=300, help_text='Brief 2-3 line summary')
    full_description = models.TextField(blank=True, help_text='Complete description of collaboration')
    objectives = models.TextField(blank=True, help_text='Objectives and scope of partnership')
    programs_activities = models.TextField(blank=True, help_text='Programs or activities conducted')
    impact_outcomes = models.TextField(blank=True, help_text='Impact and outcomes achieved')
    agreement_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    partner_website = models.URLField(blank=True, help_text='Partner organization website')
    partner_contact = models.CharField(max_length=200, blank=True)
    mou_document = models.FileField(upload_to='collaborations/mous/', blank=True, null=True, help_text='Optional downloadable MOU file')
    supporting_images = models.ImageField(upload_to='collaborations/gallery/', blank=True, null=True, help_text='Supporting image or photo')
    detail_background_color = models.CharField(
        max_length=7, blank=True, choices=BACKGROUND_COLOR_CHOICES,
        help_text='Background color for detail page. Leave blank for default.'
    )
    detail_background_image = models.ImageField(
        upload_to='collaborations/backgrounds/',
        blank=True, null=True,
        help_text='Optional background image for detail page. Shown with subtle overlay.'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-agreement_date', 'organization_name']
        verbose_name = 'Collaboration'
        verbose_name_plural = 'Collaborations'

    def __str__(self):
        return self.organization_name

    def get_absolute_url(self):
        return reverse('collaboration_detail', kwargs={'pk': self.pk})

    def mou_is_image(self):
        """Check if MOU document is an image (JPG, PNG, etc.)"""
        if not self.mou_document:
            return False
        ext = (self.mou_document.name or '').lower().split('.')[-1]
        return ext in ('jpg', 'jpeg', 'png', 'gif', 'webp')

    def mou_is_pdf(self):
        """Check if MOU document is PDF"""
        if not self.mou_document:
            return False
        return (self.mou_document.name or '').lower().endswith('.pdf')

    def get_mou_view_url(self):
        """Return URL for MOU viewer page, or None if no document"""
        if not self.mou_document:
            return None
        return reverse('collaboration_mou_view', kwargs={'pk': self.pk})
