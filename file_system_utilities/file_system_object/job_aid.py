import os
import glob

home = os.path.expanduser('~').replace('\\', '/')


def get_latest_file():
    latest_edited_folder = max(os.scandir(home), key=lambda x: x.stat().st_mtime).name
    search_on = home + '/' + latest_edited_folder + '/*'

    # return all file paths that match search pattern
    list_of_files = glob.glob(search_on)

    return max(list_of_files, key=os.path.getctime)


def get_latest_files(from_date):
    # TODO: get list of recently edited files from specified date
    pass
