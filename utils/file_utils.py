from pathlib import Path
import os
import sys
import music_tag


PROJECT_ROOT = (
    Path(sys._MEIPASS)
    if hasattr(sys, "_MEIPASS")
    else Path(__file__).resolve().parent.parent
)


def resource_path(relative_path):
    return PROJECT_ROOT / relative_path

def get_base_path():
    """محاسبه مسیر اصلی پروژه برای سازگاری با فایل اجرایی و محیط توسعه"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.getcwd()


def get_media_path(folder_name="music_files"):
    """ایجاد و بازگرداندن مسیر پوشه رسانه"""
    path = os.path.join(get_base_path(), folder_name)
    os.makedirs(path, exist_ok=True)
    return path


def extract_metadata(file_path):
    """استخراج متادیتا به صورت امن و یکپارچه"""
    try:
        mp3 = music_tag.load_file(file_path)
        return {
            "title": str(mp3["title"]) if mp3["title"] else os.path.basename(file_path),
            "length": int(mp3["#length"]) if mp3["#length"] else 1,
            "artwork": (
                mp3["artwork"].first.data
                if "artwork" in mp3 and mp3["artwork"]
                else None
            ),
            "file_path": file_path,
        }
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return {
            "title": "Unknown",
            "length": 0,
            "artwork": None,
            "file_path": file_path,
        }


def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except OSError:
        return False


# def format_time(seconds):
#     minutes = seconds // 60
#     seconds = seconds % 60
#     return f"{minutes:02d}:{seconds:02d}"

def format_time(seconds):
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"