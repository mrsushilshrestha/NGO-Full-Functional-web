from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from .models import Member, Chapter, District, Collaboration, TeamPageSettings
from apps.membership.forms import VolunteerApplicationForm
from apps.membership.models import MembershipFee


def _district_choices():
    """
    Only districts that have at least one approved volunteer.
    Prevents empty district listings and shows only active districts.
    """
    volunteer_base = Member.objects.filter(
        is_active=True, exclude_from_public=False, member_type='volunteer', district__isnull=False
    )
    district_ids = volunteer_base.values_list('district_id', flat=True).distinct()
    return [
        (d.id, d.name)
        for d in District.objects.filter(id__in=district_ids, is_active=True)
        .select_related('province')
        .order_by('province__order', 'name')
    ]


def _card_col_class(cards_per_row):
    """Bootstrap column class for member cards based on cards_per_row setting (2–5)."""
    classes = {
        2: 'col-12 col-sm-6',
        3: 'col-12 col-sm-6 col-md-4',
        4: 'col-12 col-sm-6 col-lg-3',
        5: 'col-12 col-sm-6 col-md-4 col-team-5',
    }
    return classes.get(cards_per_row, 'col-12 col-sm-6 col-md-4')


def team_board_filter(request):
    """Return board member cards HTML fragment for AJAX chapter filtering (no full page refresh)."""
    chapter_id = request.GET.get('chapter', '').strip()
    search = request.GET.get('search', '').strip()
    board = Member.objects.filter(is_active=True, exclude_from_public=False, member_type='board').order_by('order', 'name')
    if chapter_id and chapter_id.isdigit():
        board = board.filter(chapter_id=int(chapter_id))
    if search:
        board = board.filter(
            Q(name__icontains=search) |
            Q(role__icontains=search) |
            Q(member_id__icontains=search) |
            Q(specialization__icontains=search)
        )
    board = list(board[:200])
    settings = TeamPageSettings.get()
    card_col_class = _card_col_class(settings.cards_per_row)
    html = render(request, 'team/partials/board_cards.html', {
        'board_members': board,
        'card_col_class': card_col_class,
    }).content.decode()
    return HttpResponse(html, content_type='text/html; charset=utf-8')


def team_volunteer_filter(request):
    """Return volunteer cards HTML fragment for AJAX district filtering (no full page reload). Location is from district only."""
    district_id = request.GET.get('district', '').strip()
    search = request.GET.get('search', '').strip()
    volunteers = Member.objects.filter(is_active=True, exclude_from_public=False, member_type='volunteer').select_related('district').order_by('order', 'name')
    if district_id and district_id.isdigit():
        volunteers = volunteers.filter(district_id=int(district_id))
    if search:
        volunteers = volunteers.filter(
            Q(name__icontains=search) |
            Q(role__icontains=search) |
            Q(member_id__icontains=search) |
            Q(specialization__icontains=search)
        )
    volunteers = list(volunteers[:200])
    settings = TeamPageSettings.get()
    card_col_class = _card_col_class(settings.cards_per_row)
    html = render(request, 'team/partials/volunteer_cards.html', {
        'volunteers': volunteers,
        'card_col_class': card_col_class,
    }).content.decode()
    return HttpResponse(html, content_type='text/html; charset=utf-8')


def team_volunteer_page(request):
    """Return JSON with cards_html and pagination_html for AJAX pagination (no full page reload)."""
    district_filter = request.GET.get('district', '').strip()
    search = request.GET.get('search', '').strip()
    district_choices = _district_choices()
    valid_district_ids = {str(d[0]) for d in district_choices}
    if district_filter not in valid_district_ids:
        district_filter = ''

    volunteer_qs = Member.objects.filter(
        is_active=True, exclude_from_public=False, member_type='volunteer'
    ).select_related('district').order_by('order', 'name')
    if district_filter and district_filter.isdigit():
        volunteer_qs = volunteer_qs.filter(district_id=int(district_filter))
    if search:
        volunteer_qs = volunteer_qs.filter(
            Q(name__icontains=search) |
            Q(role__icontains=search) |
            Q(member_id__icontains=search) |
            Q(specialization__icontains=search)
        )

    settings = TeamPageSettings.get()
    per_page = getattr(settings, 'cards_per_page', 12) or 12
    per_page = max(6, min(24, per_page))
    paginator = Paginator(volunteer_qs, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page_number = max(1, min(int(page_number), paginator.num_pages))
    except (ValueError, TypeError):
        page_number = 1
    volunteer_page_obj = paginator.get_page(page_number)

    if paginator.num_pages <= 1:
        volunteer_pagination_range = []
    else:
        current = volunteer_page_obj.number
        pages = []
        for n in [1, *range(current - 2, current + 3), paginator.num_pages]:
            if 1 <= n <= paginator.num_pages and (not pages or n != pages[-1]):
                pages.append(n)
        volunteer_pagination_range = []
        for n in pages:
            if volunteer_pagination_range and n - volunteer_pagination_range[-1] > 1:
                volunteer_pagination_range.append(None)
            volunteer_pagination_range.append(n)

    get_dict = request.GET.copy()
    if 'page' in get_dict:
        get_dict.pop('page')
    base_query = get_dict.urlencode()

    card_col_class = _card_col_class(settings.cards_per_row)
    cards_html = render(
        request,
        'team/partials/volunteer_cards.html',
        {'volunteers': list(volunteer_page_obj.object_list), 'card_col_class': card_col_class},
    ).content.decode()

    pagination_html = render(
        request,
        'team/partials/volunteer_pagination.html',
        {
            'volunteer_page_obj': volunteer_page_obj,
            'volunteer_pagination_range': volunteer_pagination_range,
            'base_query': base_query,
        },
    ).content.decode()

    return JsonResponse({'cards_html': cards_html, 'pagination_html': pagination_html})


def team_list(request):
    team_settings = TeamPageSettings.get()
    members_qs = Member.objects.filter(is_active=True, exclude_from_public=False)
    chapter_filter = request.GET.get('chapter', '').strip()
    district_filter = request.GET.get('district', '').strip()

    # Only allow district filter for districts that actually have approved volunteers
    district_choices = _district_choices()
    valid_district_ids = {str(d[0]) for d in district_choices}
    if district_filter not in valid_district_ids:
        district_filter = ''

    member_count = members_qs.count()

    # Board: filter by chapter
    board_qs = members_qs.filter(member_type='board').order_by('order', 'name')
    if chapter_filter and chapter_filter.isdigit():
        board_qs = board_qs.filter(chapter_id=int(chapter_filter))
    board_members = list(board_qs[:200])

    # Volunteers: only from selected district when a valid district is chosen
    volunteer_qs = members_qs.filter(member_type='volunteer').select_related('district').order_by('order', 'name')
    if district_filter and district_filter.isdigit():
        volunteer_qs = volunteer_qs.filter(district_id=int(district_filter))

    # Paginate volunteers (per-page from CMS)
    per_page = getattr(team_settings, 'cards_per_page', 12) or 12
    per_page = max(6, min(24, per_page))
    paginator = Paginator(volunteer_qs, per_page)
    page_number = request.GET.get('page')
    volunteer_page_obj = paginator.get_page(page_number)

    # Build smart pagination range with ellipsis markers (None)
    if paginator.num_pages <= 1:
        volunteer_pagination_range = []
    else:
        current = volunteer_page_obj.number
        pages = []
        for n in [1, *range(current - 2, current + 3), paginator.num_pages]:
            if 1 <= n <= paginator.num_pages and (not pages or n != pages[-1]):
                pages.append(n)
        volunteer_pagination_range = []
        for n in pages:
            if volunteer_pagination_range and n - volunteer_pagination_range[-1] > 1:
                volunteer_pagination_range.append(None)
            volunteer_pagination_range.append(n)

    get_dict = request.GET.copy()
    if 'page' in get_dict:
        get_dict.pop('page')
    base_query = get_dict.urlencode()

    context = {
        'team_settings': team_settings,
        'members': members_qs,
        'board_members': board_members,
        'volunteer_page_obj': volunteer_page_obj,
        'volunteer_pagination_range': volunteer_pagination_range,
        'member_count': member_count,
        'chapters': Chapter.objects.filter(is_active=True).order_by('order', 'name'),
        'chapter_filter': chapter_filter,
        'district_choices': district_choices,
        'district_filter': district_filter,
        'volunteer_join_form': VolunteerApplicationForm(),
        'base_query': base_query,
        'card_col_class': _card_col_class(team_settings.cards_per_row),
    }
    return render(request, 'team/list.html', context)


def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk, is_active=True, exclude_from_public=False)
    return render(request, 'team/detail.html', {'member': member})


def collaboration_list(request):
    """Collaboration / Partner Wings listing page"""
    collaborations_qs = Collaboration.objects.filter(is_active=True)
    
    # Filters
    partnership_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', 'newest')
    
    if search:
        collaborations_qs = collaborations_qs.filter(
            Q(organization_name__icontains=search) |
            Q(short_description__icontains=search) |
            Q(full_description__icontains=search)
        )
    
    if partnership_type:
        collaborations_qs = collaborations_qs.filter(partnership_type=partnership_type)
    
    if status_filter:
        collaborations_qs = collaborations_qs.filter(status=status_filter)
    
    # Sorting
    if sort_by == 'oldest':
        collaborations_qs = collaborations_qs.order_by('agreement_date', 'order', 'organization_name')
    elif sort_by == 'name':
        collaborations_qs = collaborations_qs.order_by('organization_name')
    else:  # newest (default)
        collaborations_qs = collaborations_qs.order_by('-agreement_date', '-created_at', 'order', 'organization_name')
    
    # Pagination
    paginator = Paginator(collaborations_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Build pagination range
    if paginator.num_pages <= 1:
        pagination_range = []
    else:
        current = page_obj.number
        pages = []
        for n in [1, *range(current - 2, current + 3), paginator.num_pages]:
            if 1 <= n <= paginator.num_pages and (not pages or n != pages[-1]):
                pages.append(n)
        pagination_range = []
        for n in pages:
            if pagination_range and n - pagination_range[-1] > 1:
                pagination_range.append(None)
            pagination_range.append(n)
    
    return render(request, 'team/collaboration_list.html', {
        'collaborations': collaborations_qs,
        'page_obj': page_obj,
        'pagination_range': pagination_range,
        'partnership_type': partnership_type,
        'search': search,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'partnership_types': Collaboration.PARTNERSHIP_TYPE_CHOICES,
        'status_choices': Collaboration.STATUS_CHOICES,
    })


def collaboration_detail(request, pk):
    """Collaboration detail page"""
    collaboration = get_object_or_404(Collaboration, pk=pk, is_active=True)
    return render(request, 'team/collaboration_detail.html', {'collaboration': collaboration})


def collaboration_mou_view(request, pk):
    """MOU document viewer page - embeds PDF or displays image"""
    collaboration = get_object_or_404(Collaboration, pk=pk, is_active=True)
    if not collaboration.mou_document:
        from django.http import Http404
        raise Http404("No MOU document available")
    return render(request, 'team/collaboration_mou_view.html', {'collaboration': collaboration})
