# File System Utilities
Supports common use cases such as directory/file searches 

## Overview

In many projects, we often need to work with the file system to do things like recursively search through directories
to find specific types of files. We may even need to do some additional analysis on that data, extract snippets of data
or information, or simply do some type of processing on files as part of some broader data pipeline process.

## Installation


#### Using Pip from command line
`pip install git+https://github.com/kking423/file_system_utilities`

#### Using Pip using Jupyter notebook
`!pip install git+https://github.com/kking423/file_system_utilities`


## Usage
Currently, the utility is only designed to provide file system search capabilities. Simply pass a directory path, the
utility will return a dictionary of results with some additional metadata such as:
* File Size
* MIME Type
* Dates (Creation, Modified, Last Opened)
* Hidden file indicator.

The search can be customized to explicitly include or exclude results based on your given parameters. 


## Examples
The results will be returned as a dictionary so using some like a Pandas Data Frame is often useful, as shown below.

```python

from file_system_utilities.search import Search
import pandas as pd
from tabulate import tabulate

# --------------------------------------------------------
# This is a simple implementation showing the
# prettier output using Tabulate
# compared to using the standard print
# --------------------------------------------------------
# Create instance of Search object
search = Search(search_path='/projects/',
                recursive=True,
                return_all=True,
                exclude=['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git'],
                include=[])


# Output
df = pd.DataFrame(search.execute())
df = pd.concat([df, df["results"].apply(pd.Series)], axis=1)
df = df.drop(['results'], axis=1)
print(tabulate(df.head(500), headers='keys', tablefmt='psql'))

```

![](https://raw.githubusercontent.com/kking423/file_system_utilities/main/readme_resources/getting-started-with-pandas-and-tabulate.png)

<br>
<br>
<br>
<br>


#### Jupyter Notebook Example
You can use a similar approach using a Jupyter notebook. For even better experience, use JupyterLab with
<a href="https://pypi.org/project/mitosheet3/">Mito Spreadsheet</a>, a third party widget that provides excellent Excel like capabilities to interact with data. 

![](https://raw.githubusercontent.com/kking423/file_system_utilities/main/readme_resources/analysis-using-jupyterlab-and-mitosheet.png)



#### Excel Workbook Example
Extracting and manipulating data, especially larger datasets, simply work better using Python and Pandas. However,
that doesn't eliminate the need or benefit of using something like Excel to share/present data with others. Using Python
and Pandas, it's possible to automate your data analysis pipeline, which is especially ideal if you are routinely 
extracting and analyzing the same data. 

![](https://raw.githubusercontent.com/kking423/file_system_utilities/main/readme_resources/analysis-using-excel-about-page.png)

That said, I've provided an example of how to use the File System Utilities to perform a basic search, extract 
and clean the data, and then populate several spreadsheets in a single workbook. Many of these ideas can likely 
be leveraged in other datasets you are analyzing.

![](https://raw.githubusercontent.com/kking423/file_system_utilities/main/readme_resources/analysis-using-excel-multiple-worksheets.png)











