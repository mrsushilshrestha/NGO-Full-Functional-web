import json
from django.shortcuts import render
from .models import ImpactStat, ImpactDistrict


def impact(request):
    stats = ImpactStat.objects.all()
    impact_district_ids = list(ImpactDistrict.objects.values_list('district_id', flat=True))
    return render(request, 'impact/impact.html', {
        'stats': stats,
        'impact_district_ids': impact_district_ids,
        'impact_district_ids_json': json.dumps(impact_district_ids),
    })
