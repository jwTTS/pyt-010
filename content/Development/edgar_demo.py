"""
EDGAR Demo
Loads 10-K files from EDGAR for listed CIK, then processes the files looking for specified key words found
in the report text.

"""
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import requests
from lxml import html
from lxml.html import clean

from io import StringIO
import re

"""
ciks_names = {'1045810':'Nvidia',
                '789019':'Microsoft',
                '320193':'Apple',
                '1018724':'Amazon',
                '1326801':'Facebook',
                '1288776':'Google',
                '50863':'Intel',
                '2488':'AMD'
                }
"""

ciks_names = {'1045810':'Nvidia',
                '50863':'Intel',
                '2488':'AMD'
                }


years = range(2017,2020)
ciks =  list(ciks_names.keys())
qtrs = ['QTR1', 'QTR2', 'QTR3', 'QTR4']

# List of words to search
words = ['anticipate', 'believe', 'depend', 'fluctuate', 'indefinite', 'likelihood', 'possible', 'predict', 'risk', 'uncertain']

master_counts = {}

# Load index file for Year_CIK
for year in years:
    count_collection = {}
    for qtr in qtrs:
        try:
            # Load the index file for the Year_Quarter
            index_url = 'https://www.sec.gov/Archives/edgar/full-index/%s/%s/master.idx' % (year, qtr)
            print(index_url)
            sesh = requests.Session()
            page = sesh.get(index_url)

            index_stream = StringIO(str(page.content, encoding='iso-8859-2'))
            index_df = pd.read_csv(index_stream, sep="|", header=5, low_memory=False)
        except:
            print("Cannot Load Index: " + index_url)
            break
        
        for cik in ciks:    
            
            print("Company: " + ciks_names[cik])

            filename = index_df[((index_df['CIK']==cik) & (index_df['Form Type']=='10-K'))]['Filename']

            if not(filename.empty):

                filename = filename.to_string(index=False).strip()

                # Create URL String
                url = "https://www.sec.gov/Archives/%s" % filename

                # Load Page
                sesh = requests.Session()
                page = sesh.get(url)

                if page.status_code != 200:
                    print("File not found: " + url)
                else:
                    # Parse the html document and cleanout page structure/formating etc.
                    doc = html.fromstring(page.content)
                    doc = clean.Cleaner().clean_html(doc)

                    # Extract only text from the HTML and split into lines
                    lines = doc.text_content().splitlines()

                    # Initalize the count dictionary
                    word_counts = {}
                    for word in words:
                        word_counts[word] = 0

                    for line in lines:
                        clean_line = re.sub(r'[^a-zA-Z0-9_ ]','',line)
                        for word in words:
                            word_counts[word] = word_counts[word] + clean_line.count(word)

                    count_collection[cik] = word_counts
    master_counts[year] = count_collection

print("Done getting Data")

df_rows = []

for year in years:
    for key in master_counts[year].keys():
        df_row = {}
        df_row['year'] = year
        df_row['cik'] = key
        df_row['company_name'] = ciks_names[key]
        df_row.update(master_counts[year][key])
        df_rows.append(df_row)

df = pd.DataFrame(df_rows, columns = df_row.keys())

df_melt = pd.melt(df, id_vars=['year', 'company_name'], value_vars=words)

g = sns.catplot(x='year', y='value', hue='variable',col='company_name', kind='point', data=df_melt, ci=None)
plt.show()