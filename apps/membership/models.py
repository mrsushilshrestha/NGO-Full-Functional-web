from django.db import models


class MembershipFee(models.Model):
    """Editable membership fees"""
    MEMBER_TYPE_CHOICES = [
        ('general', 'General Member'),
        ('active', 'Active Member'),
    ]
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.get_member_type_display()}: NPR {self.amount}'


class VolunteerApplication(models.Model):
    """Volunteer application form submissions"""
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='volunteers/', blank=True, null=True)
    location = models.CharField(max_length=200)
    availability = models.CharField(max_length=300)
    past_experience = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending',
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return self.name


class MembershipApplication(models.Model):
    """Membership application form submissions"""
    MEMBER_TYPE_CHOICES = [
        ('general', 'General Member'),
        ('active', 'Active Member'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('esewa', 'eSewa'),
        ('khalti', 'Khalti'),
        ('bank', 'Bank Transfer'),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_reference = models.CharField(max_length=200, blank=True, help_text='Transaction UUID or pidx for payment tracking')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending',
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return self.name
