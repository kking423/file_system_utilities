from file_system_utilities.search import Search
import pandas as pd
from tabulate import tabulate

# --------------------------------------------------------
# This is a simple implementation showing the
# prettier output using Tabulate
# compared to using the standard print
# --------------------------------------------------------
# Create instance of Search object
search = Search(search_path='/users/kyleking/projects/file_system_utilities',
                recursive=True,
                return_all=True,
                exclude=['.map', 'venv', '.pyc', '__pycache__', '.DS_Store', 'ignore', '.idea', 'git'],
                include=[])


# Output
df = pd.DataFrame(search.execute())
df = pd.concat([df, df["results"].apply(pd.Series)], axis=1)
df = df.drop(['results'], axis=1)
print(tabulate(df.head(500), headers='keys', tablefmt='psql'))

