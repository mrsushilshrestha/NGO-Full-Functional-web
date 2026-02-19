from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Member, Chapter, Collaboration
from apps.membership.forms import VolunteerApplicationForm, MembershipApplicationForm
from apps.membership.models import MembershipFee


def team_list(request):
    members_qs = Member.objects.filter(is_active=True)
    search = request.GET.get('search', '')
    chapter_filter = request.GET.get('chapter', '')
    view_mode = request.GET.get('view', 'grid')

    if search:
        members_qs = members_qs.filter(
            Q(name__icontains=search) |
            Q(role__icontains=search) |
            Q(member_id__icontains=search) |
            Q(specialization__icontains=search)
        )
    if chapter_filter:
        members_qs = members_qs.filter(chapter_id=chapter_filter)

    member_count = members_qs.count()

    executive_members = members_qs.filter(role_level='executive')
    core_members = members_qs.filter(role_level='core')
    general_qs = members_qs.filter(role_level='general')

    paginator = Paginator(general_qs, 8)
    page_number = request.GET.get('page')
    general_page_obj = paginator.get_page(page_number)

    # Build smart pagination range with ellipsis markers (None)
    if paginator.num_pages <= 1:
        general_pagination_range = []
    else:
        current = general_page_obj.number
        pages = []
        for n in [1, *range(current - 2, current + 3), paginator.num_pages]:
            if 1 <= n <= paginator.num_pages and (not pages or n != pages[-1]):
                pages.append(n)
        general_pagination_range = []
        for n in pages:
            if general_pagination_range and n - general_pagination_range[-1] > 1:
                general_pagination_range.append(None)
            general_pagination_range.append(n)

    context = {
        'members': members_qs,
        'executive_members': executive_members,
        'core_members': core_members,
        'general_page_obj': general_page_obj,
        'general_pagination_range': general_pagination_range,
        'member_count': member_count,
        'chapters': Chapter.objects.all(),
        'search': search,
        'chapter_filter': chapter_filter,
        'view_mode': view_mode,
        'volunteer_join_form': VolunteerApplicationForm(),
        'membership_join_form': MembershipApplicationForm(),
        'membership_fees': MembershipFee.objects.all(),
    }
    return render(request, 'team/list.html', context)


def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk, is_active=True)
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
