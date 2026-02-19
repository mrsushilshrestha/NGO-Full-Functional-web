"""Image processing utilities - resize/crop to aspect ratio."""
import io
from PIL import Image
from django.core.files.base import ContentFile


def process_image_to_aspect_ratio(image_field, target_ratio='16:9', quality=85):
    """
    Crop/resize image to target aspect ratio (e.g. 16:9).
    Modifies the image_field in place.
    """
    if not image_field:
        return
    try:
        img = Image.open(image_field).convert('RGB')
    except Exception:
        return
    w, h = img.size
    target_w, target_h = map(int, target_ratio.split(':'))
    current_ratio = w / h
    target_ratio_val = target_w / target_h

    if abs(current_ratio - target_ratio_val) < 0.01:
        # Already close enough
        return

    if current_ratio > target_ratio_val:
        # Image is wider - crop width
        new_w = int(h * target_ratio_val)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Image is taller - crop height
        new_h = int(w / target_ratio_val)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    output = io.BytesIO()
    fmt = 'JPEG'  # Use JPEG for smaller size
    save_kw = {'format': fmt, 'quality': quality, 'optimize': True}
    img.save(output, **save_kw)
    output.seek(0)
    name = image_field.name.rsplit('.', 1)[0] + '.jpg'
    image_field.save(name, ContentFile(output.read()), save=False)
