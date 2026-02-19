from django.shortcuts import render
from .models import OrganizationInfo, Founder, ChapterLocation, Achievement


def about(request):
    org = OrganizationInfo.objects.first()
    founders = Founder.objects.all()
    chapters = ChapterLocation.objects.all()
    achievements = Achievement.objects.all()

    return render(request, 'about/about.html', {
        'org': org,
        'founders': founders,
        'chapters': chapters,
        'achievements': achievements,
    })
