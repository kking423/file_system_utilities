__all__ = ['FileSystemObject']

import os
import cv2
import mimetypes
import pathlib
from datetime import datetime, timezone, date
import numpy as np


class FileSystemObject:
    IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')

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
        self.matrix_score: int = self.get_image_matrix(path, compression=50, allowed=self.IMAGE_EXTENSIONS)

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

    @staticmethod
    def get_image_matrix(path, compression, allowed: tuple = IMAGE_EXTENSIONS):
        try:
            if path.lower().endswith(allowed):
                img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if type(img) == np.ndarray:
                    img = img[..., 0:3]
                    img = cv2.resize(img, dsize=(compression, compression), interpolation=cv2.INTER_CUBIC)
                    return np.sum(img)
                else:
                    return 0
            else:
                return 0
        except:
            return 0

    @staticmethod
    def compare_images_from_matrix(img1, img2):
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img2.shape[1])
        return err
