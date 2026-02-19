from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.http import require_GET, require_POST
from .decorators import cms_required
from .forms import (
    HeroBannerForm, HomeContentForm, AnnouncementPopupForm, GalleryImageForm,
    OrganizationInfoForm, FounderForm, ChapterLocationForm, AchievementForm,
    ImpactStatForm, ContactInfoForm, DonationTierForm, BankDetailForm, IconConfigForm,
    NavItemForm, SiteThemeForm, SiteIdentityForm, MemberForm, ProgramForm,
    QuickResponseForm, ChatSettingsForm, CollaborationForm,
)

# Core models
from apps.core.models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage, NavItem, SiteTheme, SiteIdentity
# About models
from apps.about.models import OrganizationInfo, Founder, ChapterLocation, Achievement
# Programs
from apps.programs.models import Program, Category
# Team
from apps.team.models import Member, Chapter, Collaboration
# Impact
from apps.impact.models import ImpactStat
# Contact
from apps.contact.models import ContactInfo, ContactMessage, ChatMessage, QuickResponse, ChatSettings
# Donation
from apps.donation.models import DonationTier, Donation, BankDetail
# Membership
from apps.membership.models import MembershipFee, VolunteerApplication, MembershipApplication
# CMS
from apps.cms.models import CMSNotification, IconConfig


def cms_login(request):
    """Custom CMS login at /admin-login"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('cms_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', None)
            return redirect(next_url or 'cms_dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'cms/login.html')


def cms_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('cms_login')


# Notifications API
@cms_required
def cms_notifications_api(request):
    """Return notifications as JSON for dropdown."""
    from django.http import JsonResponse
    notifications = CMSNotification.objects.all()[:15]
    data = [{'id': n.id, 'type': n.notification_type, 'title': n.title, 'message': n.message[:80] if n.message else '', 'link': n.link, 'is_read': n.is_read, 'created': n.created_at.isoformat()} for n in notifications]
    return JsonResponse({'notifications': data, 'unread_count': CMSNotification.objects.filter(is_read=False).count()})


@cms_required
def cms_notification_mark_read(request, pk):
    """Mark single notification as read."""
    from django.http import JsonResponse
    n = CMSNotification.objects.filter(pk=pk).first()
    if n:
        n.is_read = True
        n.save()
    return JsonResponse({'ok': True})


@cms_required
@require_POST
def cms_notification_mark_all_read(request):
    """Mark all notifications as read."""
    from django.http import JsonResponse
    CMSNotification.objects.filter(is_read=False).update(is_read=True)
    return JsonResponse({'ok': True})


@cms_required
@require_GET
def cms_dashboard(request):
    """CMS Dashboard with stats and quick links"""
    stats = {
        'programs': Program.objects.count(),
        'members': Member.objects.filter(is_active=True).count(),
        'donations': Donation.objects.filter(status='completed').count(),
        'messages': ContactMessage.objects.count(),
    }
    return render(request, 'cms/dashboard.html', {'stats': stats})


# Home / Core
@cms_required
@require_GET
def cms_home(request):
    banners = HeroBanner.objects.all()
    contents = HomeContent.objects.all()
    announcements = AnnouncementPopup.objects.all()
    gallery = GalleryImage.objects.all()
    return render(request, 'cms/home.html', {
        'banners': banners,
        'contents': contents,
        'announcements': announcements,
        'gallery': gallery,
    })


@cms_required
@require_GET
def cms_about(request):
    org = OrganizationInfo.objects.first()
    founders = Founder.objects.all()
    chapters = ChapterLocation.objects.all()
    achievements = Achievement.objects.all()
    return render(request, 'cms/about.html', {
        'org': org,
        'founders': founders,
        'chapters': chapters,
        'achievements': achievements,
    })


@cms_required
@require_GET
def cms_programs(request):
    programs = Program.objects.all()
    return render(request, 'cms/programs.html', {'programs': programs})


@cms_required
@require_GET
def cms_team(request):
    members = Member.objects.all()
    chapters = Chapter.objects.all()
    collaborations = Collaboration.objects.all()
    return render(request, 'cms/team.html', {'members': members, 'chapters': chapters, 'collaborations': collaborations})


@cms_required
@require_GET
def cms_impact(request):
    stats = ImpactStat.objects.all()
    return render(request, 'cms/impact.html', {'stats': stats})


@cms_required
@require_GET
def cms_contact(request):
    info = ContactInfo.objects.first()
    messages_list = ContactMessage.objects.all()[:20]
    return render(request, 'cms/contact.html', {'info': info, 'contact_messages': messages_list})


@cms_required
@require_GET
def cms_donation(request):
    tiers = DonationTier.objects.all()
    bank_details = BankDetail.objects.all()
    return render(request, 'cms/donation.html', {'tiers': tiers, 'bank_details': bank_details})


@cms_required
@require_GET
def cms_members(request):
    """Member/volunteer approval center."""
    volunteers = VolunteerApplication.objects.all()[:50]
    members = MembershipApplication.objects.all()[:50]
    return render(request, 'cms/members.html', {'volunteers': volunteers, 'members': members})


@cms_required
@require_POST
def cms_member_action(request, model_type, pk, action):
    """Approve or reject a volunteer or membership application."""
    if model_type == 'volunteer':
        obj = get_object_or_404(VolunteerApplication, pk=pk)
    elif model_type == 'membership':
        obj = get_object_or_404(MembershipApplication, pk=pk)
    else:
        messages.error(request, 'Invalid request.')
        return redirect('cms_members')
    if action in ('approve', 'reject'):
        obj.status = action + 'd'  # approved / rejected
        obj.save()
        msg = f'{obj.name} {action}d successfully.'
        messages.success(request, msg)
        CMSNotification.objects.create(
            notification_type='member_approved' if action == 'approve' else 'member_rejected',
            title=f'{obj.__class__.__name__.replace("Application", "")} {action}d: {obj.name}',
            message=msg,
            link='/admin-login/members/',
        )
    return redirect('cms_members')


# Edit views
@cms_required
def cms_banner_edit(request, pk=None):
    obj = get_object_or_404(HeroBanner, pk=pk) if pk else None
    if request.method == 'POST':
        form = HeroBannerForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner saved!')
            return redirect('cms_home')
    else:
        form = HeroBannerForm(instance=obj)
    return render(request, 'cms/banner_edit.html', {'form': form, 'title': 'Edit Banner' if obj else 'Add Banner', 'back_url': 'cms_home'})


@cms_required
def cms_banner_delete(request, pk):
    obj = get_object_or_404(HeroBanner, pk=pk)
    obj.delete()
    messages.success(request, 'Banner deleted.')
    return redirect('cms_home')


@cms_required
def cms_content_edit(request, pk=None):
    obj = get_object_or_404(HomeContent, pk=pk) if pk else None
    if request.method == 'POST':
        form = HomeContentForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content saved!')
            return redirect('cms_home')
    else:
        form = HomeContentForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Content' if obj else 'Add Content', 'back_url': 'cms_home'})


@cms_required
def cms_announcement_edit(request, pk=None):
    obj = get_object_or_404(AnnouncementPopup, pk=pk) if pk else None
    if request.method == 'POST':
        form = AnnouncementPopupForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement saved!')
            return redirect('cms_home')
    else:
        form = AnnouncementPopupForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Announcement' if obj else 'Add Announcement', 'back_url': 'cms_home', 'form_type': 'announcement'})


@cms_required
def cms_gallery_edit(request, pk=None):
    obj = get_object_or_404(GalleryImage, pk=pk) if pk else None
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image saved!')
            return redirect('cms_home')
    else:
        form = GalleryImageForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Image' if obj else 'Add Image', 'back_url': 'cms_home'})


@cms_required
def cms_org_edit(request):
    obj = OrganizationInfo.objects.first()
    if not obj:
        obj = OrganizationInfo()
    if request.method == 'POST':
        form = OrganizationInfoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization info saved!')
            return redirect('cms_about')
    else:
        form = OrganizationInfoForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Organization Info', 'back_url': 'cms_about'})


@cms_required
def cms_founder_edit(request, pk=None):
    obj = get_object_or_404(Founder, pk=pk) if pk else None
    if request.method == 'POST':
        form = FounderForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Founder saved!')
            return redirect('cms_about')
    else:
        form = FounderForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Founder' if obj else 'Add Founder', 'back_url': 'cms_about'})


@cms_required
def cms_chapter_edit(request, pk=None):
    obj = get_object_or_404(ChapterLocation, pk=pk) if pk else None
    if request.method == 'POST':
        form = ChapterLocationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter saved!')
            return redirect('cms_about')
    else:
        form = ChapterLocationForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Chapter' if obj else 'Add Chapter', 'back_url': 'cms_about'})


@cms_required
def cms_achievement_edit(request, pk=None):
    obj = get_object_or_404(Achievement, pk=pk) if pk else None
    if request.method == 'POST':
        form = AchievementForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Achievement saved!')
            return redirect('cms_about')
    else:
        form = AchievementForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Achievement' if obj else 'Add Achievement', 'back_url': 'cms_about'})


@cms_required
def cms_impact_edit(request, pk=None):
    obj = get_object_or_404(ImpactStat, pk=pk) if pk else None
    if request.method == 'POST':
        form = ImpactStatForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impact stat saved!')
            return redirect('cms_impact')
    else:
        form = ImpactStatForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Stat' if obj else 'Add Stat', 'back_url': 'cms_impact'})


@cms_required
def cms_contact_edit(request):
    obj = ContactInfo.objects.first()
    if not obj:
        obj = ContactInfo()
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact info saved!')
            return redirect('cms_contact')
    else:
        form = ContactInfoForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Contact Info', 'back_url': 'cms_contact'})


@cms_required
def cms_tier_edit(request, pk=None):
    obj = get_object_or_404(DonationTier, pk=pk) if pk else None
    if request.method == 'POST':
        form = DonationTierForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation tier saved!')
            return redirect('cms_donation')
    else:
        form = DonationTierForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Tier' if obj else 'Add Tier', 'back_url': 'cms_donation'})


@cms_required
def cms_bank_edit(request, pk=None):
    obj = get_object_or_404(BankDetail, pk=pk) if pk else None
    if request.method == 'POST':
        form = BankDetailForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank detail saved!')
            return redirect('cms_donation')
    else:
        form = BankDetailForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Bank' if obj else 'Add Bank', 'back_url': 'cms_donation'})


@cms_required
@require_GET
def cms_icons(request):
    icons = IconConfig.objects.all()
    return render(request, 'cms/icons.html', {'icons': icons})


@cms_required
def cms_icon_edit(request, pk):
    obj = get_object_or_404(IconConfig, pk=pk)
    if request.method == 'POST':
        form = IconConfigForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Icon saved!')
            return redirect('cms_icons')
    else:
        form = IconConfigForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': f'Edit {obj.get_location_display()}', 'back_url': 'cms_icons'})


def _ensure_default_nav_children():
    """Ensure Programs has Gallery child (on hover) and Team has Collaborations child."""
    programs = NavItem.objects.filter(url='/programs/', parent__isnull=True).first()
    old = programs.children.filter(url='/programs/gallery/').first() if programs else None
    if old:
        old.url = '/gallery/'
        old.save()
    if programs and not programs.children.filter(url='/gallery/').exists():
        NavItem.objects.get_or_create(
            url='/gallery/', parent=programs,
            defaults={'title': 'Gallery', 'icon_class': 'fas fa-images', 'order': 0, 'is_active': True}
        )
    # Ensure Team has Collaborations child
    team = NavItem.objects.filter(url='/team/', parent__isnull=True).first()
    if team and not team.children.filter(url='/team/collaborations/').exists():
        NavItem.objects.get_or_create(
            url='/team/collaborations/', parent=team,
            defaults={'title': 'Collaboration / Partner Wings', 'icon_class': 'fas fa-handshake', 'order': 0, 'is_active': True}
        )


# Site Navigation Settings
@cms_required
@require_GET
def cms_navigation(request):
    _ensure_default_nav_children()
    items = NavItem.objects.filter(parent__isnull=True).prefetch_related('children')
    return render(request, 'cms/navigation.html', {'nav_items': items})


@cms_required
def cms_nav_edit(request, pk=None):
    obj = get_object_or_404(NavItem, pk=pk) if pk else None
    if request.method == 'POST':
        form = NavItemForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nav item saved!')
            return redirect('cms_navigation')
    else:
        form = NavItemForm(instance=obj)
    return render(request, 'cms/navigation_edit.html', {'form': form, 'title': 'Edit Nav' if obj else 'Add Nav', 'obj': obj})


@cms_required
@require_POST
def cms_nav_delete(request, pk):
    obj = get_object_or_404(NavItem, pk=pk)
    obj.delete()
    messages.success(request, 'Nav item deleted.')
    return redirect('cms_navigation')


@cms_required
@require_POST
def cms_nav_reorder(request):
    from django.http import JsonResponse
    order = request.POST.getlist('order[]')
    for i, pk in enumerate(order):
        NavItem.objects.filter(pk=pk).update(order=i)
    return JsonResponse({'ok': True})


@cms_required
@require_POST
def cms_nav_restore_defaults(request):
    """Restore default navigation items with children: Programs→Gallery, Contact→Chat with us, Terms→Members"""
    from django.utils import timezone
    defaults_parents = [
        ('Home', '/', 'fas fa-home', 0, False),
        ('About', '/about/', 'fas fa-info-circle', 1, False),
        ('Programs', '/programs/', 'fas fa-calendar-alt', 2, False),
        ('Team', '/team/', 'fas fa-users', 3, False),
        ('Impact', '/impact/', 'fas fa-chart-line', 4, False),
        ('Contact', '/contact/', 'fas fa-envelope', 5, False),
        ('Donate', '/donate/', 'fas fa-heart', 6, True),
    ]
    created_count = 0
    for title, url, icon, order, is_btn in defaults_parents:
        obj, created = NavItem.objects.get_or_create(
            url=url, parent__isnull=True,
            defaults={'title': title, 'icon_class': icon, 'order': order, 'is_button': is_btn, 'parent': None}
        )
        if created:
            created_count += 1
    # Remove/deactivate Contact and Team children (revert to old plain nav)
    contact = NavItem.objects.filter(url='/contact/', parent__isnull=True).first()
    if contact:
        contact.children.update(is_active=False)
    team = NavItem.objects.filter(url='/team/', parent__isnull=True).first()
    if team:
        team.children.update(is_active=False)
    # Child items: Programs→Gallery only (shows on hover)
    programs = NavItem.objects.filter(url='/programs/', parent__isnull=True).first()
    if programs:
        c, created = NavItem.objects.get_or_create(
            url='/gallery/', parent=programs,
            defaults={'title': 'Gallery', 'icon_class': 'fas fa-images', 'order': 0, 'is_active': True}
        )
        if not created:
            c.is_active = True
            c.parent = programs
            c.title = 'Gallery'
            c.icon_class = 'fas fa-images'
            c.save()
        if created:
            created_count += 1
    messages.success(request, f'Restored default navigation ({created_count} new items).')
    return redirect('cms_navigation')


# Site theme / colors
@cms_required
def cms_theme(request):
    theme = SiteTheme.get()
    if request.method == 'POST':
        if request.POST.get('action') == 'reset':
            theme.primary_color = '#0B5345'
            theme.secondary_color = '#148f77'
            theme.nav_bg_color = '#0B5345'
            theme.nav_text_color = '#ffffff'
            theme.nav_hover_color = 'rgba(255,255,255,0.15)'
            theme.button_color = '#c17f59'
            theme.button_hover_color = '#a86d4a'
            theme.dark_mode_enabled = False
            theme.dark_bg_color = '#1a1a1a'
            theme.dark_text_color = '#e0e0e0'
            theme.dark_card_bg = '#2d2d2d'
            theme.save()
            messages.success(request, 'Theme reset to defaults.')
            return redirect('cms_theme')
        form = SiteThemeForm(request.POST, instance=theme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Theme saved!')
            return redirect('cms_theme')
    else:
        form = SiteThemeForm(instance=theme)
    return render(request, 'cms/theme.html', {'form': form, 'theme': theme})


# Site Identity
@cms_required
def cms_identity(request):
    identity = SiteIdentity.get()
    if request.method == 'POST':
        if request.POST.get('action') == 'reset':
            identity.site_title = 'NHAF Nepal'
            identity.tagline = ''
            identity.logo = None
            identity.favicon = None
            identity.save()
            messages.success(request, 'Identity reset to defaults.')
            return redirect('cms_identity')
        form = SiteIdentityForm(request.POST, request.FILES, instance=identity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site identity saved!')
            return redirect('cms_identity')
    else:
        form = SiteIdentityForm(instance=identity)
    return render(request, 'cms/identity.html', {'form': form, 'identity': identity})


# Member Management
@cms_required
@require_GET
def cms_member_management(request):
    members = Member.objects.all()
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role__icontains=role_filter)
    return render(request, 'cms/member_management.html', {'members': members, 'role_filter': role_filter})


@cms_required
def cms_member_edit(request, pk=None):
    obj = get_object_or_404(Member, pk=pk) if pk else None
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member saved!')
            return redirect('cms_member_management')
    else:
        form = MemberForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Member' if obj else 'Add Member', 'back_url': 'cms_member_management'})


@cms_required
@require_POST
def cms_member_delete(request, pk):
    obj = get_object_or_404(Member, pk=pk)
    obj.delete()
    messages.success(request, 'Member deleted.')
    return redirect('cms_member_management')


# Collaboration Management
@cms_required
@require_GET
def cms_collaboration_management(request):
    collaborations = Collaboration.objects.all()
    type_filter = request.GET.get('type', '')
    if type_filter:
        collaborations = collaborations.filter(partnership_type=type_filter)
    return render(request, 'cms/collaboration_management.html', {
        'collaborations': collaborations,
        'type_filter': type_filter,
        'partnership_types': Collaboration.PARTNERSHIP_TYPE_CHOICES,
    })


@cms_required
def cms_collaboration_edit(request, pk=None):
    obj = get_object_or_404(Collaboration, pk=pk) if pk else None
    if request.method == 'POST':
        form = CollaborationForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collaboration saved!')
            return redirect('cms_collaboration_management')
    else:
        form = CollaborationForm(instance=obj)
    return render(request, 'cms/edit_form.html', {
        'form': form,
        'title': 'Edit Collaboration' if obj else 'Add Collaboration',
        'back_url': 'cms_collaboration_management'
    })


@cms_required
@require_POST
def cms_collaboration_delete(request, pk):
    obj = get_object_or_404(Collaboration, pk=pk)
    obj.delete()
    messages.success(request, 'Collaboration deleted.')
    return redirect('cms_collaboration_management')


# Program Management
@cms_required
@require_GET
def cms_program_management(request):
    programs = Program.objects.all()
    return render(request, 'cms/program_management.html', {'programs': programs})


@cms_required
def cms_program_edit(request, pk=None):
    obj = get_object_or_404(Program, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProgramForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program saved!')
            return redirect('cms_program_management')
    else:
        form = ProgramForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Program' if obj else 'Add Program', 'back_url': 'cms_program_management'})


@cms_required
@require_POST
def cms_program_delete(request, pk):
    obj = get_object_or_404(Program, pk=pk)
    obj.delete()
    messages.success(request, 'Program deleted.')
    return redirect('cms_program_management')


def _chatsettings_columns(request):
    """Return set of contact_chatsettings column names (for optional fields)."""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(contact_chatsettings)")
            return {row[1] for row in cursor.fetchall()}
    except Exception:
        return set()


# Unified Chat (single CMS page: settings + quick responses + live conversations)
@cms_required
def cms_chat(request):
    from django.utils import timezone
    from django.db import connection
    settings = ChatSettings.get()
    try:
        settings.admin_last_seen = timezone.now()
        settings.save(update_fields=['admin_last_seen'])
    except Exception:
        pass
    cols = _chatsettings_columns(request)
    def strip_missing_fields(form):
        if 'default_quick_response_id' not in cols and 'default_quick_response' in form.fields:
            del form.fields['default_quick_response']
        if 'chat_mode' not in cols and 'chat_mode' in form.fields:
            del form.fields['chat_mode']
        if 'whatsapp_phone' not in cols and 'whatsapp_phone' in form.fields:
            del form.fields['whatsapp_phone']
        if 'custom_chat_link' not in cols and 'custom_chat_link' in form.fields:
            del form.fields['custom_chat_link']
    if request.method == 'POST' and request.POST.get('section') == 'settings':
        form = ChatSettingsForm(request.POST, instance=settings)
        strip_missing_fields(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chat settings saved!')
            return redirect('cms_chat')
    else:
        form = ChatSettingsForm(instance=settings)
        strip_missing_fields(form)
    sessions_raw = ChatMessage.objects.values('session_id', 'sender_name', 'sender_email').distinct()
    sessions_list = []
    for s in sessions_raw:
        last_msg = ChatMessage.objects.filter(session_id=s['session_id']).order_by('-created_at').first()
        unread = ChatMessage.objects.filter(session_id=s['session_id'], sender_type='user', is_read=False).count()
        sessions_list.append({
            'session_id': s['session_id'],
            'name': s['sender_name'] or 'Anonymous',
            'email': s['sender_email'] or '',
            'last_message': last_msg.message[:50] if last_msg else '',
            'last_time': last_msg.created_at if last_msg else None,
            'unread_count': unread,
        })
    sessions_list.sort(key=lambda x: x['last_time'] or x['session_id'], reverse=True)
    responses = QuickResponse.objects.all()
    try:
        has_trigger_keywords = hasattr(QuickResponse.objects.first(), 'trigger_keywords') if QuickResponse.objects.exists() else hasattr(QuickResponse(), 'trigger_keywords')
    except Exception:
        has_trigger_keywords = False
    return render(request, 'cms/chat.html', {
        'form': form, 'settings': settings, 'sessions': sessions_list, 'responses': responses, 'has_trigger_keywords': has_trigger_keywords,
    })


# Live Chat (kept for direct URL / backwards compatibility)
@cms_required
@require_GET
def cms_live_chat(request):
    from django.utils import timezone
    s = ChatSettings.get()
    s.admin_last_seen = timezone.now()
    s.save(update_fields=['admin_last_seen'])
    sessions = ChatMessage.objects.values('session_id', 'sender_name', 'sender_email').distinct()
    sessions_list = []
    for s in sessions:
        last_msg = ChatMessage.objects.filter(session_id=s['session_id']).order_by('-created_at').first()
        unread = ChatMessage.objects.filter(session_id=s['session_id'], sender_type='user', is_read=False).count()
        sessions_list.append({
            'session_id': s['session_id'],
            'name': s['sender_name'] or 'Anonymous',
            'email': s['sender_email'] or '',
            'last_message': last_msg.message[:50] if last_msg else '',
            'last_time': last_msg.created_at if last_msg else None,
            'unread_count': unread,
        })
    sessions_list.sort(key=lambda x: x['last_time'] or x['session_id'], reverse=True)
    return render(request, 'cms/live_chat.html', {'sessions': sessions_list})


@cms_required
def cms_chat_session(request, session_id):
    from django.utils import timezone
    s = ChatSettings.get()
    s.admin_last_seen = timezone.now()
    s.save(update_fields=['admin_last_seen'])
    messages_list = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
    ChatMessage.objects.filter(session_id=session_id, sender_type='user', is_read=False).update(is_read=True)
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            ChatMessage.objects.create(
                session_id=session_id,
                sender_type='admin',
                sender_name=request.user.username,
                message=msg
            )
            return redirect('cms_chat_session', session_id=session_id)
    return render(request, 'cms/chat_session.html', {'session_id': session_id, 'messages': messages_list})


@cms_required
@require_GET
def cms_chat_api(request, session_id):
    from django.http import JsonResponse
    messages_list = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
    data = [{'id': m.id, 'sender': m.sender_type, 'name': m.sender_name, 'message': m.message, 'time': m.created_at.isoformat()} for m in messages_list]
    return JsonResponse({'messages': data})


@cms_required
@require_POST
def cms_chat_send(request, session_id):
    from django.http import JsonResponse
    msg = request.POST.get('message', '').strip()
    if msg:
        ChatMessage.objects.create(
            session_id=session_id,
            sender_type='admin',
            sender_name=request.user.username,
            message=msg
        )
    return JsonResponse({'ok': True})


# Quick Responses
@cms_required
@require_GET
def cms_quick_responses(request):
    responses = QuickResponse.objects.all()
    settings = ChatSettings.get()
    return render(request, 'cms/quick_responses.html', {'responses': responses, 'settings': settings})


@cms_required
def cms_quick_response_edit(request, pk=None):
    obj = get_object_or_404(QuickResponse, pk=pk) if pk else None
    if request.method == 'POST':
        form = QuickResponseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quick response saved!')
            return redirect('cms_quick_responses')
    else:
        form = QuickResponseForm(instance=obj)
    return render(request, 'cms/edit_form.html', {'form': form, 'title': 'Edit Response' if obj else 'Add Response', 'back_url': 'cms_quick_responses'})


@cms_required
@require_POST
def cms_quick_response_delete(request, pk):
    obj = get_object_or_404(QuickResponse, pk=pk)
    obj.delete()
    messages.success(request, 'Quick response deleted.')
    return redirect('cms_quick_responses')


@cms_required
@require_POST
def cms_quick_response_reorder(request):
    from django.http import JsonResponse
    order = request.POST.getlist('order[]')
    for i, pk in enumerate(order):
        QuickResponse.objects.filter(pk=pk).update(order=i)
    return JsonResponse({'ok': True})


@cms_required
def cms_chat_settings(request):
    settings = ChatSettings.get()
    if request.method == 'POST':
        form = ChatSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chat settings saved!')
            return redirect('cms_chat_settings')
    else:
        form = ChatSettingsForm(instance=settings)
    return render(request, 'cms/chat_settings.html', {'form': form, 'settings': settings})
