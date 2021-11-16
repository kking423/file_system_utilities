from search import Search
from datetime import datetime, timezone
import json
import pandas as pd
import numpy as np
import time
import openpyxl
from openpyxl.styles import Font, Fill

# Global variables
df: pd.DataFrame
report_file = f"file-search-results-{datetime.today().strftime('%Y-%m-%d')}.xlsx"
workbook_objects = []

# Customize Search Settings
# Create instance of Search object
search = Search(search_path='/users/kyleking/projects/file_system_utilities',
                recursive=True,
                return_all=True,
                exclude=['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git'],
                include=[])


def get_search_results():
    global df
    df = pd.DataFrame(search.execute())
    df = pd.concat([df, df["results"].apply(pd.Series)], axis=1)
    df = df.drop(['results'], axis=1)


def transform_results():
    fix_missing_values()
    add_size_classification()
    add_file_aging_classification()


def generate_report_data():
    # Output (order of list prior to export will dictate the sheet order)
    add_about_page()
    add_search_results()

    add_pivot_by_file_aging_and_type()
    add_pivot_by_file_size()

    add_pivot_by_folder_aging_and_type()
    add_pivot_by_folder_size()

    export_to_excel(report_file)
    update_about_page()


def fix_missing_values():
    # Fix Missing/NaN values
    df['file_mime_type'] = df['file_mime_type'].fillna('Not Available')


def add_size_classification():
    conditions = [
        (df['size_mb'] <= 1),  # Very Small [<1 MB]
        (df['size_mb'] <= 10),  # Small [1-10 MB]
        (df['size_mb'] <= 100),  # Medium [10-100 MB]
        (df['size_mb'] <= 1000),  # Large [100-1000 MB]
        (df['size_mb'] > 1000),  # Very Large [> 1000 MB]
    ]

    choices = ['Very Small [<1 MB]',
               'Small [1-10 MB]',
               'Medium [10-100 MB]',
               'Large [100-1000 MB]',
               'Very Large [> 1000 MB]']

    df['size_classification'] = np.select(conditions, choices)


def add_file_aging_classification():
    conditions = [
        (df['age'] <= 1),  # <=1 Year
        (df['age'] <= 3),  # 1-3 Years
        (df['age'] <= 5),  # 3-5 Years
        (df['age'] <= 7),  # 5-7 Years
        (df['age'] <= 10),  # 7-10 Years
        (df['age'] <= 15),  # 10-15 Years
        (df['age'] <= 20),  # 15-20 Years
        (df['age'] <= 30),  # 20-30 Years
        (df['age'] > 30),  # 30+ Years

    ]

    choices = ['<=1 Year',
               '1-3 Years',
               '3-5 Years',
               '5-7 Years',
               '7-10 Years',
               '10-15 Years',
               '15-20 Years',
               '20-30 Years',
               '30+ Years']

    df['aging_tier'] = np.select(conditions, choices)
    # print(tabulate(output, headers='keys', tablefmt='psql'))


def add_pivot_by_file_aging_and_type():
    pivot = pd.pivot_table(data=df,
                           index=['file_extension', 'file_mime_type', ],
                           columns=['aging_tier'],
                           aggfunc=['count'],
                           values=['file'],
                           fill_value=0,
                           margins=True)

    workbook_objects.append({'SheetName': 'File Aging Summary',
                             'Object': pivot,
                             'StartRow': 4,
                             'StartCol': 1
                             })


def add_pivot_by_folder_aging_and_type():
    pivot = pd.pivot_table(data=df,
                           index=['folder'],
                           columns=['aging_tier'],
                           aggfunc=['count'],
                           values=['full_path'],
                           fill_value=0,
                           margins=True)

    workbook_objects.append({'SheetName': 'Folder Aging Summary',
                             'Object': pivot,
                             'StartRow': 4,
                             'StartCol': 1
                             })


def add_pivot_by_file_size():
    pivot = pd.pivot_table(data=df,
                           index=['file_extension', 'file_mime_type', ],
                           columns=['size_classification'],
                           aggfunc=['count'],
                           values=['file'],
                           fill_value=0,
                           margins=True)

    workbook_objects.append({'SheetName': 'File Size Summary',
                             'Object': pivot,
                             'StartRow': 4,
                             'StartCol': 1
                             })


def add_pivot_by_folder_size():
    pivot = pd.pivot_table(data=df,
                           index=['folder'],
                           columns=['size_classification'],
                           aggfunc=['count'],
                           values=['full_path'],
                           fill_value=0,
                           margins=True)

    workbook_objects.append({'SheetName': 'Folder Size Summary',
                             'Object': pivot,
                             'StartRow': 4,
                             'StartCol': 1
                             })


def add_search_results():
    workbook_objects.append({'SheetName': 'Search Results',
                             'Object': df,
                             'StartRow': 0,
                             'StartCol': 0
                             })


def add_about_page():
    search_criteria = {
        'Search Criteria': search.to_dict()
    }

    workbook_objects.append({'SheetName': 'About',
                             'Object': pd.DataFrame(search_criteria),
                             'StartRow': 6,
                             'StartCol': 1
                             })


def update_about_page():
    # TODO: this needs some improvement; not sure openpyxl is the way to go here
    workbook = openpyxl.load_workbook(report_file)
    worksheet = workbook['About']
    worksheet['B2'] = 'Search Results'
    worksheet['B3'] = 'Purpose:'
    worksheet['C3'] = 'Show all results of a file system search based on customized search criteria'
    worksheet['B4'] = 'Run Date'
    worksheet['C4'] = datetime.today()
    worksheet['B5'] = 'Total Results Found:'
    worksheet['C5'] = str(df.shape[0])  # row count

    c = worksheet['B2']
    c.font = Font(size=22, bold=True)
    workbook.save(report_file)


def export_to_excel(report_name):
    # utc is not supported in Excel so need to remove from dataframe during this step
    df['created_dt'] = df['created_dt'].dt.tz_localize(None)
    df['modified_dt'] = df['modified_dt'].dt.tz_localize(None)
    df['opened_dt'] = df['opened_dt'].dt.tz_localize(None)

    workbook_objects.append({'SheetName': 'Search Results',
                             'Object': df,
                             'StartRow': 0,
                             'StartCol': 0
                             })

    with pd.ExcelWriter(report_name) as writer:
        for obj in workbook_objects:
            obj['Object'].to_excel(writer, sheet_name=obj['SheetName'],
                                   startrow=obj['StartRow'],
                                   startcol=obj['StartCol'])

            sheet = writer.sheets['About']
            sheet.set_column('B:C', 40)


if __name__ == '__main__':
    get_search_results()
    transform_results()
    generate_report_data()





