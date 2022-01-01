__all__ = ['Search']

import os
import file_system_utilities.file_system_object as fso_meta
from file_system_utilities.file_system_object import FileSystemObject


class Search:
    def __init__(self, search_path: str = '..',
                 recursive=True,
                 return_all=True,
                 exclude: list = None,
                 include: list = None):

        self.search_path = search_path
        self.recursive = recursive
        self.return_all = return_all
        self.exclusion_list = exclude
        self.inclusion_list = include

        self._is_match = True  # if not all, include only match; if all, append all
        self._results = {'results': []}

    def to_dict(self):
        return {
            'Search Path': self.search_path,
            'Recursive': self.recursive,
            'Return All': self.return_all,
            'Exclusion List': self.exclusion_list,
            'Inclusion List': self.inclusion_list
        }

    def __repr__(self):
        return f'Search(search_path="{self.search_path}"'

    def _evaluate_match_criteria(self, path):
        excludes = all(path.lower().find(criteria.lower()) <= 0 for criteria in self.exclusion_list)
        includes = any(path.lower().find(criteria.lower()) > 0 for criteria in self.inclusion_list)

        self._is_match = excludes or includes

    def execute(self):
        for root, folders, files in os.walk(self.search_path, topdown=True):
            if not self.recursive and root != self.search_path:
                break  # discontinue loop if we don't need to evaluate any lower

            self._search_folders(root, files)
            self._search_files(root, files)

        return self._results

    def _search_folders(self, root, files):
        # iterate and evaluate each folder

        fso = FileSystemObject(root)
        meta = fso_meta

        self._evaluate_match_criteria(root)
        fso.__setattr__("search_match", self._is_match)

        # calculate file size of each folder
        for file in files:
            file_path = os.path.join(root, file)
            if meta.get_is_file(file_path):

                fso.file_count += 1
                fso.size += meta.get_size(file_path)
                fso.size_kb += meta.get_size_kb(file_path)
                fso.size_mb += meta.get_size_mb(file_path)
                fso.size_gb += meta.get_size_gb(file_path)

        if self.return_all or self._is_match:
            self._results['results'].append(fso.to_dict())

    def _search_files(self, root, files):
        for file in files:
            file_path = os.path.join(root, file)

            fso = FileSystemObject(file_path)

            self._evaluate_match_criteria(file_path)
            fso.__setattr__("search_match", self._is_match)

            fso.file_count += 1

            if self.return_all or self._is_match:
                self._results['results'].append(fso.to_dict())


