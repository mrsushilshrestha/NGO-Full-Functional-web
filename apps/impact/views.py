from django.shortcuts import render
from .models import ImpactStat


def impact(request):
    stats = ImpactStat.objects.all()
    return render(request, 'impact/impact.html', {'stats': stats})
