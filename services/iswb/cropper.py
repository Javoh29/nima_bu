from PIL import Image
import numpy as np
from uuid import uuid4
import os
from django.conf import settings

class Cropper:
    def crop_image(self, image_path: str, bbox: list) -> str:
        image = Image.open(image_path)
        file_extension = image.format.lower()
        cropped_image = image.crop(bbox)
        crop_dir = os.path.join(settings.MEDIA_ROOT, "photos", "crop")
        os.makedirs(crop_dir, exist_ok=True)
        cropped_filename = f"image_{uuid4()}.{file_extension}"
        cropped_path = os.path.join(crop_dir, cropped_filename)
        cropped_image.save(cropped_path, format=image.format)
        return cropped_path
