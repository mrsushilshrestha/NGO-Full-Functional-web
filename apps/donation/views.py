import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import DonationTier, Donation, BankDetail
from .forms import DonationForm
from .services import get_esewa_form_data, initiate_khalti_payment, verify_khalti_payment


def _get_base_url(request):
    """Build base URL for callbacks."""
    scheme = 'https' if request.is_secure() else 'http'
    return f"{scheme}://{request.get_host()}"


def donate(request):
    tiers = DonationTier.objects.all()
    bank_details = BankDetail.objects.all()
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = form.cleaned_data['payment_method']
            donor_name = form.cleaned_data.get('donor_name', '')
            donor_email = form.cleaned_data.get('donor_email', '')

            if payment_method == 'bank':
                donation = Donation.objects.create(
                    amount=amount,
                    donor_name=donor_name,
                    donor_email=donor_email,
                    payment_method='bank',
                    status='pending',
                )
                return render(request, 'donation/bank_details.html', {
                    'donation': donation,
                    'bank_details': bank_details,
                })

            if payment_method == 'esewa':
                base_url = _get_base_url(request)
                transaction_uuid = f'don-{Donation.objects.count() + 1}-{uuid.uuid4().hex[:8]}'
                form_data = get_esewa_form_data(
                    amount=amount,
                    success_url=f'{base_url}{reverse("donate_esewa_success", kwargs={"tid": transaction_uuid})}',
                    failure_url=f'{base_url}{reverse("donate_esewa_failure", kwargs={"tid": transaction_uuid})}',
                    transaction_uuid=transaction_uuid,
                )
                donation = Donation.objects.create(
                    amount=amount,
                    donor_name=donor_name,
                    donor_email=donor_email,
                    payment_method='esewa',
                    payment_reference=form_data['transaction_uuid'],
                    status='pending',
                )
                return render(request, 'donation/esewa_form.html', {
                    'form_data': form_data,
                    'esewa_url': settings.ESEWA_PAYMENT_URL,
                    'donation': donation,
                })

            if payment_method == 'khalti':
                if not settings.KHALTI_SECRET_KEY:
                    messages.error(request, 'Khalti payment is not configured. Please use eSewa or Bank Transfer.')
                    return redirect('donate')
                base_url = _get_base_url(request)
                amount_paisa = int(float(amount) * 100)
                purchase_order_id = f'donate-{Donation.objects.count() + 1}'
                payment_url, pidx = initiate_khalti_payment(
                    amount_paisa=amount_paisa,
                    return_url=f'{base_url}{reverse("donate_khalti_return")}',
                    purchase_order_id=purchase_order_id,
                    purchase_order_name='NHAF Nepal Donation',
                    customer_info={'name': donor_name or 'Donor', 'email': donor_email or ''},
                )
                if payment_url:
                    donation = Donation.objects.create(
                        amount=amount,
                        donor_name=donor_name,
                        donor_email=donor_email,
                        payment_method='khalti',
                        pidx=pidx,
                        payment_reference=purchase_order_id,
                        status='pending',
                    )
                    return redirect(payment_url)
                messages.error(request, f'Khalti error: {pidx}')
        else:
            messages.error(request, 'Please correct the form errors.')
    else:
        form = DonationForm()
    return render(request, 'donation/donate.html', {
        'form': form,
        'tiers': tiers,
    })


def donate_esewa_success(request, tid):
    """eSewa success callback."""
    donation = Donation.objects.filter(payment_reference=tid, payment_method='esewa').first()
    if donation:
        donation.status = 'completed'
        donation.transaction_id = request.GET.get('refId', '') or tid
        donation.save()
    return redirect('donate_thanks')


def donate_esewa_failure(request, tid):
    """eSewa failure callback."""
    Donation.objects.filter(payment_reference=tid, payment_method='esewa').update(status='failed')
    messages.warning(request, 'Payment was not completed.')
    return redirect('donate')


def donate_khalti_return(request):
    """Khalti return callback - verify via lookup then redirect."""
    pidx = request.GET.get('pidx')
    status = request.GET.get('status')
    if not pidx:
        messages.warning(request, 'Invalid payment response.')
        return redirect('donate')
    donation = Donation.objects.filter(pidx=pidx, payment_method='khalti').first()
    if not donation:
        messages.warning(request, 'Donation record not found.')
        return redirect('donate')
    verify_status, data = verify_khalti_payment(pidx)
    if verify_status == 'Completed':
        donation.status = 'completed'
        donation.transaction_id = data.get('transaction_id', '')
        donation.save()
        return redirect('donate_thanks')
    if status == 'User canceled':
        donation.status = 'canceled'
        donation.save()
    messages.warning(request, 'Payment was not completed.')
    return redirect('donate')


def donate_thanks(request):
    return render(request, 'donation/thanks.html')
