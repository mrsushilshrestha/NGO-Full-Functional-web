import json
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q, Case, When, Value, IntegerField
from .models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage
from apps.programs.models import Program
from apps.team.models import Collaboration


def home(request):
    banners = HeroBanner.objects.filter(is_active=True)
    contents = {c.key: c for c in HomeContent.objects.filter(is_active=True)}
    now = timezone.now()
    announcements = AnnouncementPopup.objects.filter(
        status='published', is_active=True
    ).filter(
        Q(start_date__isnull=True) | Q(start_date__lte=now)
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    ).annotate(
        priority_order=Case(
            When(priority='high', then=Value(0)),
            When(priority='medium', then=Value(1)),
            When(priority='low', then=Value(2)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('priority_order', '-start_date', '-id')
    gallery = GalleryImage.objects.filter(is_active=True)[:12]
    programs = Program.objects.all()[:6]
    collaborations = Collaboration.objects.filter(is_active=True).order_by('order', '-agreement_date', 'organization_name')

    ann_json = json.dumps([
        {'id': a.id, 'title': a.title, 'message': a.message,
         'image': a.image.url if a.image else '', 'link_url': a.link_url or '', 'link_text': a.link_text or 'Learn More'}
        for a in announcements
    ])
    return render(request, 'core/home.html', {
        'banners': banners,
        'contents': contents,
        'announcements': announcements,
        'announcements_json': ann_json,
        'gallery': gallery,
        'programs': programs,
        'collaborations': collaborations,
    })
