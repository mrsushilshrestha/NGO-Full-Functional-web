from django.db import models


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
