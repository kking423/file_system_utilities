__all__ = ['FileSystemObject']


import os
import mimetypes
import pathlib
from datetime import datetime, timezone, date


class FileSystemObject:
    def __init__(self, path):
        self.full_path: str = path
        self.object_type: str = self.get_object_type(path)
        self.is_hidden: bool = self.is_hidden(path)
        self.folder: str = self.get_folder_name(path)
        self.file: str = self.get_file_name(path)
        self.file_extension: str = self.get_file_extension(path)
        self.file_mime_type: str = self.get_mime_type(path)
        self.file_count: int = 0
        self.size: int = self.get_size(path)
        self.size_kb: float = self.get_size_kb(path)
        self.size_mb: float = self.get_size_mb(path)
        self.size_gb: float = self.get_size_gb(path)
        self.created_dt: datetime = self.get_creation_date(path)
        self.modified_dt: datetime = self.get_modified_date(path)
        self.opened_dt: datetime = self.get_opened_date(path)
        self.owner: str = self.get_owner(path)
        self.group: str = self.get_group(path)
        self.age: int = self.get_age_in_years(self.created_dt.date())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def get_folder_name(path):
        if os.path.isdir(path):
            return os.path.basename(os.path.normpath(path))

    @staticmethod
    def get_file_name(path):
        if os.path.isfile(path):
            return os.path.basename(os.path.normpath(path))

    @staticmethod
    def get_creation_date(path):
        return datetime.fromtimestamp(os.stat(path).st_birthtime, tz=timezone.utc)

    @staticmethod
    def get_modified_date(path):
        return datetime.fromtimestamp(os.stat(path).st_mtime, tz=timezone.utc)

    @staticmethod
    def get_opened_date(path):
        return datetime.fromtimestamp(os.stat(path).st_atime, tz=timezone.utc)

    @staticmethod
    def get_size(path):
        if os.path.isfile(path):
            return os.stat(path).st_size
        else:
            return 0

    @staticmethod
    def get_size_kb(path):
        if os.path.isfile(path):
            size = os.stat(path).st_size
            return round(size / 1024, 3)
        else:
            return 0

    @staticmethod
    def get_size_mb(path):
        if os.path.isfile(path):
            size = os.stat(path).st_size
            return round(size / (1024 * 1024), 3)
        else:
            return 0

    @staticmethod
    def get_size_gb(path):
        if os.path.isfile(path):
            size = os.stat(path).st_size
            return round(size / (1024 * 1024 * 1024), 3)
        else:
            return 0

    @staticmethod
    def get_file_extension(path):
        if os.path.isfile(path):
            return pathlib.Path(path).suffix.lower()
        else:
            return None

    @staticmethod
    def get_mime_type(path):
        if os.path.isfile(path):
            return mimetypes.guess_type(path, strict=False)[0]
        else:
            return None

    @staticmethod
    def get_object_type(path):
        if os.path.isdir(path):
            return "Folder"
        else:
            return "File"
        # return os.path.isdir(path)

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)

    @staticmethod
    def is_hidden(path):
        basename = os.path.basename(os.path.normpath(path))
        return basename[0] == '.'

    @staticmethod
    def get_owner(path):
        return pathlib.Path(path).owner()

    @staticmethod
    def get_group(path):
        return pathlib.Path(path).group()

    @staticmethod
    def get_age_in_years(eval_date):
        days_in_year = 365.2425
        return int((date.today() - eval_date).days / days_in_year)
