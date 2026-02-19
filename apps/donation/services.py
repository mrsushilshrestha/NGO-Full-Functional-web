"""Payment gateway integration services."""
import hmac
import hashlib
import base64
import uuid
import requests
from django.conf import settings


def generate_esewa_signature(total_amount, transaction_uuid, product_code):
    """Generate HMAC-SHA256 signature for eSewa."""
    secret = settings.ESEWA_SECRET_KEY
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = base64.b64encode(
        hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()
    return signature


def get_esewa_form_data(amount, success_url, failure_url, transaction_uuid=None):
    """Build eSewa payment form data."""
    product_code = settings.ESEWA_MERCHANT_ID
    transaction_uuid = transaction_uuid or str(uuid.uuid4())
    total_amount = str(int(float(amount)))
    signature = generate_esewa_signature(total_amount, transaction_uuid, product_code)
    return {
        'amount': total_amount,
        'tax_amount': '0',
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid,
        'product_code': product_code,
        'product_service_charge': '0',
        'product_delivery_charge': '0',
        'success_url': success_url,
        'failure_url': failure_url,
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
        'signature': signature,
    }


def initiate_khalti_payment(amount_paisa, return_url, purchase_order_id, purchase_order_name, customer_info=None):
    """Initiate Khalti payment and return payment_url."""
    if not settings.KHALTI_SECRET_KEY:
        return None, 'Khalti not configured'
    url = settings.KHALTI_API_URL
    headers = {
        'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    website_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'
    website_url = f'http://{website_url}' if not website_url.startswith('http') else website_url
    payload = {
        'return_url': return_url,
        'website_url': website_url,
        'amount': int(amount_paisa),
        'purchase_order_id': purchase_order_id,
        'purchase_order_name': purchase_order_name,
        'customer_info': customer_info or {},
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        data = r.json()
        if r.status_code == 200 and data.get('payment_url'):
            return data.get('payment_url'), data.get('pidx')
        return None, data.get('detail', str(data))
    except Exception as e:
        return None, str(e)


def verify_khalti_payment(pidx):
    """Verify Khalti payment via lookup API."""
    if not settings.KHALTI_SECRET_KEY:
        return None, 'Khalti not configured'
    url = settings.KHALTI_API_URL.rsplit('/', 1)[0] + '/lookup/'
    headers = {
        'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    try:
        r = requests.post(url, json={'pidx': pidx}, headers=headers, timeout=10)
        data = r.json()
        if r.status_code == 200:
            return data.get('status'), data
        return None, data
    except Exception as e:
        return None, {'error': str(e)}
