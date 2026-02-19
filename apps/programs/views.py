from django.shortcuts import render
from django.db.models import Q
from .models import Program


def programs_list(request):
    programs = Program.objects.all()
    category_filter = request.GET.get('category', '')
    sort = request.GET.get('sort', 'desc')

    if category_filter:
        programs = programs.filter(category=category_filter)
    if sort == 'asc':
        programs = programs.order_by('event_date')
    else:
        programs = programs.order_by('-event_date')

    upcoming = programs.filter(category='upcoming')
    past = programs.filter(category='past')

    return render(request, 'programs/list.html', {
        'programs': programs,
        'upcoming': upcoming,
        'past': past,
        'category_filter': category_filter,
        'sort': sort,
    })


def program_detail(request, slug):
    program = Program.objects.get(slug=slug)
    return render(request, 'programs/detail.html', {'program': program})
