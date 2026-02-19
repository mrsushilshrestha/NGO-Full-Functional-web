"""Process hero banner images to aspect ratio on save."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HeroBanner
from .utils import process_image_to_aspect_ratio


@receiver(post_save, sender=HeroBanner)
def process_hero_banner_image(sender, instance, created, **kwargs):
    """Crop hero banner image to configured aspect ratio (default 16:9)."""
    if getattr(instance, '_image_processed', False) or not instance.image:
        return
    try:
        process_image_to_aspect_ratio(instance.image, instance.aspect_ratio)
        instance._image_processed = True
        instance.save(update_fields=['image'])
    except Exception:
        pass
