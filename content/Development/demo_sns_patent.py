"""
Seaborn Example - Patent Data
"""

# import packages

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% Loading WIPO Patent data and melting into Tidy data

patent = pd.read_csv('ExData/patent_data.csv', header=6)

patent.head(6)

new_columns = patent.iloc[0, : 4].values.tolist()
new_columns.extend(patent.columns[4:])
patent.columns = new_columns

patent.drop(0, inplace = True)

patent.head()

patent_melt = pd.melt(patent, id_vars=['Office', 'Technology'], value_vars=['2010', '2011', '2012'])
patent_melt .columns = ['country', 'class', 'year', 'number_patents']

# %% Total Patents for all countries
g = sns.catplot(x='country', y='number_patents',
                data=patent_melt,
                kind='bar', col='year', ci=None)
g.set_xticklabels(rotation=90)
g.fig.suptitle('Patent Counts by Country')
plt.show()

# %% Total Patents for Canada and USA only
g = sns.catplot(x='country', y='number_patents',
                data=patent_melt [(patent_melt['country'] == 'Canada') | (patent_melt['country'] == 'United States of America')],
                kind='bar', col='year', ci=None)
g.set_xticklabels(rotation=90)
g.fig.suptitle('Patent Counts by Country')
plt.show()

# %% Total Patents by technology category for Canada and USA only
g = sns.catplot(x='country', y='number_patents',
                data=patent_melt[(patent_melt['country'] == 'Canada') | (patent_melt['country'] == 'United States of America')],
                kind='bar', col='year', ci=None, hue = 'class')
g.set_xticklabels(rotation=90)
g.fig.suptitle('Patent Counts by Country')
plt.show()