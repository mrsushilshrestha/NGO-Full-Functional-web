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
    if request.method == 'POST':
        form = VolunteerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your volunteer application has been submitted.')
            return redirect('team_list')
    else:
        form = VolunteerApplicationForm()
    return render(request, 'membership/volunteer_form.html', {'form': form})


def membership_form(request):
    fees = MembershipFee.objects.all()
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            fee = fees.filter(member_type=app.member_type).first()
            amount = fee.amount if fee else 0
            app.amount_paid = amount

            if app.payment_method == 'bank':
                app.save()
                bank_details = BankDetail.objects.all()
                messages.success(request, 'Application submitted. Please complete bank transfer.')
                return render(request, 'membership/bank_transfer.html', {
                    'app': app,
                    'bank_details': bank_details,
                })

            if app.payment_method == 'esewa':
                app.save()
                base_url = _get_base_url(request)
                transaction_uuid = f'memb-{app.id}-{uuid.uuid4().hex[:8]}'
                app.payment_reference = transaction_uuid
                app.save()
                form_data = get_esewa_form_data(
                    amount=amount,
                    success_url=f'{base_url}{reverse("membership_esewa_success", kwargs={"tid": transaction_uuid})}',
                    failure_url=f'{base_url}{reverse("membership_esewa_failure", kwargs={"tid": transaction_uuid})}',
                    transaction_uuid=transaction_uuid,
                )
                return render(request, 'donation/esewa_form.html', {
                    'form_data': form_data,
                    'esewa_url': settings.ESEWA_PAYMENT_URL,
                })

            if app.payment_method == 'khalti':
                if not settings.KHALTI_SECRET_KEY:
                    messages.error(request, 'Khalti is not configured. Use eSewa or Bank Transfer.')
                    return redirect('membership_form')
                app.save()
                base_url = _get_base_url(request)
                amount_paisa = int(float(amount) * 100)
                purchase_order_id = f'memb-{app.id}'
                payment_url, pidx = initiate_khalti_payment(
                    amount_paisa=amount_paisa,
                    return_url=f'{base_url}{reverse("membership_khalti_return")}',
                    purchase_order_id=purchase_order_id,
                    purchase_order_name=f'NHAF Membership - {app.get_member_type_display()}',
                    customer_info={'name': app.name, 'email': app.email, 'phone': app.phone},
                )
                if payment_url and pidx:
                    app.payment_reference = pidx
                    app.save()
                    return redirect(payment_url)
                messages.error(request, f'Khalti error: {pidx}')
                return redirect('membership_form')

            app.save()
            messages.success(request, 'Thank you! Your membership application has been submitted.')
            return redirect('team_list')
    else:
        form = MembershipApplicationForm()
    return render(request, 'membership/membership_form.html', {'form': form, 'fees': fees})


def membership_esewa_success(request, tid):
    app = MembershipApplication.objects.filter(payment_reference=tid).first()
    if app:
        app.status = 'approved'
        app.save()
    messages.success(request, 'Payment successful! Your membership application has been received.')
    return redirect('team_list')


def membership_esewa_failure(request, tid):
    messages.warning(request, 'Payment was not completed.')
    return redirect('membership_form')


def membership_khalti_return(request):
    pidx = request.GET.get('pidx')
    if not pidx:
        messages.warning(request, 'Invalid payment response.')
        return redirect('membership_form')
    app = MembershipApplication.objects.filter(payment_reference=pidx).first()
    if not app:
        messages.warning(request, 'Application not found.')
        return redirect('membership_form')
    status, data = verify_khalti_payment(pidx)
    if status == 'Completed':
        app.status = 'approved'
        app.save()
        messages.success(request, 'Payment successful! Your membership application has been received.')
    else:
        messages.warning(request, 'Payment was not completed.')
    return redirect('team_list')
