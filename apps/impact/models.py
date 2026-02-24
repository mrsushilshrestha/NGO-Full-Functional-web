from django.db import models


class ImpactDistrict(models.Model):
    """Districts/regions where the NGO has impact - shown on the Nepal map (SVG id)."""
    district_id = models.CharField(
        max_length=20,
        unique=True,
        help_text='Must match SVG path id (e.g. NPBA, NPKA, NPLU). See map regions: Karnali, Mahakali, Seti, Dhawalagiri, Gandaki, Bagmati, Janakpur, Sagarmatha, Bhojpur, Mechi, Narayani, Lumbini, Rapti, Bheri.'
    )
    display_name = models.CharField(max_length=100, blank=True, help_text='Optional override for legend/tooltip')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'district_id']

    def __str__(self):
        return self.display_name or self.district_id


class ImpactStat(models.Model):
    """Impact statistics with animated counters"""
    label = models.CharField(max_length=200)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=20, blank=True, help_text='e.g. +, K, M')
    icon = models.CharField(max_length=100, blank=True, help_text='FontAwesome class e.g. fa-users')
    tagline = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.label}: {self.value}{self.suffix}'
