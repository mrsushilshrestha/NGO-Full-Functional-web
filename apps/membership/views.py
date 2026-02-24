import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import MembershipFee, MembershipApplication
from .forms import VolunteerApplicationForm, MembershipApplicationForm
from apps.donation.services import get_esewa_form_data, initiate_khalti_payment, verify_khalti_payment
from apps.donation.models import BankDetail


def _get_base_url(request):
    return f"{'https' if request.is_secure() else 'http'}://{request.get_host()}"


def membership_index(request):
    return redirect('team_list')


def volunteer_form(request):
    """Volunteer form - same as application_center (volunteer only)."""
    return application_center(request)


def application_center(request):
    """
    Volunteer application only. Uses design from commented code.
    No General Member form displayed. Join Us content from TeamPageSettings (CMS).
    """
    from apps.team.models import Province, District, TeamPageSettings
    team_settings = TeamPageSettings.get()
    form = VolunteerApplicationForm()
    provinces = Province.objects.filter(is_active=True).order_by('order')
    districts_by_province = {}
    for p in provinces:
        districts_by_province[p.id] = list(
            District.objects.filter(province=p, is_active=True).order_by('name').values('id', 'name')
        )
    import json
    districts_json = json.dumps(districts_by_province)

    selected_district_id = None
    selected_province_id = None
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your volunteer application has been submitted.')
            return redirect('application_status', app_type='volunteer', status='pending')
        # Repopulate province/district from POST so dropdowns restore on validation error
        district_id_raw = request.POST.get('district')
        if district_id_raw:
            try:
                d = District.objects.get(pk=int(district_id_raw))
                selected_district_id = d.id
                selected_province_id = d.province_id
            except (District.DoesNotExist, ValueError, TypeError):
                pass
    else:
        form = VolunteerApplicationForm()

    return render(request, 'membership/volunteer_apply.html', {
        'form': form,
        'provinces': provinces,
        'districts_json': districts_json,
        'selected_district_id': selected_district_id,
        'selected_province_id': selected_province_id,
        'team_settings': team_settings,
    })


def application_status(request, app_type, status):
    """MODIFICATION: Show application status message (Pending/Approved/Rejected)."""
    status_messages = {
        'pending': 'Your application is under review.',
        'approved': 'Congratulations! Your application has been approved.',
        'rejected': 'Sorry, your application was not approved.',
    }
    msg = status_messages.get(status, 'Your application is under review.')
    return render(request, 'membership/application_status.html', {
        'status': status,
        'message': msg,
        'app_type': app_type,
    })


def membership_form(request):
    """Legacy: redirect to unified application center."""
    return redirect('application_center')


def membership_esewa_success(request, tid):
    app = MembershipApplication.objects.filter(payment_reference=tid).first()
    if app:
        app.status = 'approved'
        app.save()
    messages.success(request, 'Payment successful! Your membership application has been received.')
    return redirect('team_list')


def membership_esewa_failure(request, tid):
    messages.warning(request, 'Payment was not completed.')
    return redirect('application_center')


def membership_khalti_return(request):
    pidx = request.GET.get('pidx')
    if not pidx:
        messages.warning(request, 'Invalid payment response.')
        return redirect('application_center')
    app = MembershipApplication.objects.filter(payment_reference=pidx).first()
    if not app:
        messages.warning(request, 'Application not found.')
        return redirect('application_center')
    status, data = verify_khalti_payment(pidx)
    if status == 'Completed':
        app.status = 'approved'
        app.save()
        messages.success(request, 'Payment successful! Your membership application has been received.')
    else:
        messages.warning(request, 'Payment was not completed.')
    return redirect('team_list')
