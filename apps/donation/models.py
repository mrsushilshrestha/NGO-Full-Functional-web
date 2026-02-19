from django.db import models


class DonationTier(models.Model):
    """Donation amount tiers"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    label = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'amount']

    def __str__(self):
        return f'NPR {self.amount} - {self.label or "Donation"}'


class BankDetail(models.Model):
    """Bank details for transfer - CMS editable"""
    bank_name = models.CharField(max_length=200)
    account_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=100)
    branch = models.CharField(max_length=200, blank=True)
    swift_code = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.bank_name} - {self.account_number}'


class Donation(models.Model):
    """Donation records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('bank', 'Bank Transfer'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donor_name = models.CharField(max_length=200, blank=True)
    donor_email = models.EmailField(blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=200, blank=True)
    pidx = models.CharField(max_length=100, blank=True, help_text='Khalti payment ID')
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'NPR {self.amount} - {self.donor_name or "Anonymous"}'
