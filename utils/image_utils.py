import os
from PIL import Image
import io
from .file_utils import get_media_path


def save_artwork_cache(artwork_bytes, track_id):
    """ذخیره بایت‌های تصویر در دیتابیس به صورت فایل کش برای سرعت بیشتر"""
    if not artwork_bytes:
        return None

    cache_dir = get_media_path(os.path.join("cache", "artworks"))
    file_name = f"art_{track_id}.png"
    file_path = os.path.join(cache_dir, file_name)

    if not os.path.exists(file_path):
        try:
            image = Image.open(io.BytesIO(artwork_bytes))
            image.load()

            if image.width > 1000 or image.height > 1000:
                image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

            image.save(file_path, "WEBP", quality=85)

        except Exception as e:
            print(f"Image cache error: {e}")
            return None

    return file_path
