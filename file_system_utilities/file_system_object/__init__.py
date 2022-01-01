__all__ = ['FileSystemObject']


import os
import mimetypes
import pathlib
import glob
from datetime import datetime, timezone, date


home = os.path.expanduser('~').replace('\\', '/')


def get_latest_file():
    latest_edited_folder = max(os.scandir(home), key=lambda x: x.stat().st_mtime).name
    search_on = home + '/' + latest_edited_folder + '/*'

    # return all file paths that match search pattern
    list_of_files = glob.glob(search_on)

    return max(list_of_files, key=os.path.getctime)


def get_folder_name(path):
    if os.path.isdir(path):
        return os.path.basename(os.path.normpath(path))


def get_folder_path(path):
    return os.path.dirname(os.path.abspath(path))


def get_file_name(path):
    if os.path.isfile(path):
        return os.path.basename(os.path.normpath(path))


def get_creation_date(path):
    modified_date = datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)
    birth_date = datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)
    if birth_date > modified_date:
        return modified_date
    else:
        return birth_date


def get_modified_date(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)


def get_opened_date(path):
    return datetime.fromtimestamp(os.stat(path).st_atime, tz=timezone.utc)


def get_size(path):
    if os.path.isfile(path):
        return os.stat(path).st_size
    else:
        return 0


def get_size_kb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / 1024, 3)
    else:
        return 0


def get_size_mb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / 1024**2, 3)
    else:
        return 0


def get_size_gb(path):
    if os.path.isfile(path):
        size = os.stat(path).st_size
        return round(size / (1024**2 * 1024), 3)
    else:
        return 0


def get_file_extension(path):
    if os.path.isfile(path):
        return pathlib.Path(path).suffix.lower()
    else:
        return None


def get_mime_type(path):
    if os.path.isfile(path):
        return mimetypes.guess_type(path, strict=False)[0]
    else:
        return None


def get_object_type(path):
    if os.path.isdir(path):
        return "Folder"
    else:
        return "File"


def get_is_file(path):
    return os.path.isfile(path)


def get_is_image(path):
    img_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw', '.jpg', '.png', '.gif', '.jpeg']
    file_extension = get_file_extension(path)
    mime_type = str(get_mime_type(path)).lower().startswith('image')

    return mime_type or file_extension in img_formats


def get_is_video(path):
    return str(get_mime_type(path)).lower().startswith('video')


def get_is_raw_image(path):
    raw_formats = ['.raw', '.dng', '.heic', '.sr2', '.orf', '.crw']
    file_extension = get_file_extension(path)
    # valid_extension = [item for item in raw_formats if (item.lower() == file_extension)]

    return file_extension in raw_formats


def get_is_hidden(path):
    return os.path.basename(os.path.normpath(path))[0] == '.'


def get_owner(path):
    return pathlib.Path(path).owner()


def get_group(path):
    return pathlib.Path(path).group()


def get_age_in_years(eval_date):
    days_in_year = 365.2425
    return int((date.today() - eval_date).days / days_in_year)


class FileSystemObject:
    def __init__(self, path):
        self.full_path: str = path
        self.object_type: str = get_object_type(path)
        self.is_hidden: bool = get_is_hidden(path)
        self.folder: str = get_folder_name(path)
        self.file: str = get_file_name(path)
        self.file_extension: str = get_file_extension(path)
        self.file_mime_type: str = get_mime_type(path)
        self.file_count: int = 0
        self.size: int = get_size(path)
        self.size_kb: float = get_size_kb(path)
        self.size_mb: float = get_size_mb(path)
        self.size_gb: float = get_size_gb(path)
        self.created_dt: datetime = get_creation_date(path)
        self.modified_dt: datetime = get_modified_date(path)
        self.opened_dt: datetime = get_opened_date(path)
        self.owner: str = get_owner(path)
        self.group: str = get_group(path)
        self.age: int = get_age_in_years(self.modified_dt.date())

    def to_dict(self):
        return self.__dict__

