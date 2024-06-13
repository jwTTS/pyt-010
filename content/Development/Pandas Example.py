# 1. Importing and Preparing Data with Pandas
# 
# Data preparation is an important step before any analysis of the data. This includes:
# - Importing the data form various sources (Excel files, Web Scraping, etc.)
# - Cleaning up the data (removing any NA's, deleting extra rows/columns not needed
# - Aggregating multiple sources (merging or concatenating tables)
# - Any sorting or filtering of data

# <font color = 'blue'> **Import Packages and File** </font>
# 
# There are several ways to import Excel files using Pandas:
# - Loading a CSV file using read_csv or Excel file using read_excel
# - The path of the file can be given in "absolute" or "relative" terms to your project directory.
# 
# Below is an example of loading the file using the absolute path.

# In[2]:


import pandas as pd
#newDF = pd.read_excel(r'C:\Users\guido\Desktop\Python Class\Excel\Data Manipulation Worksheet.xlsx', sheet_name='Financing Table')


# Below is the alternative way using relative path (note, only one of these lines of codes actually needs to be run). Before running the code below, ensure there is an "ExData" folder in the same project folder as this Jupyter file.

# In[4]:


newDF = pd.read_excel('../ExData/Data Manipulation Worksheet.xlsx', sheet_name='Financing Table')


# <font color = 'blue'> **Check and Clean Data** </font>
# - Using **df.shape** can quickly tell us the # of rows and columns in our data set
#     - In example below, it is stating we have 568 rows of data
# - Using **df.head()** can help us see the first 5 rows of data
#     - A value can be given in brackets to show more rows (e.g. head(10) will show first 10 rows) 
# - Another useful method is **df.info()** which will list all the column headers, along with how many data points we have in each column, and what type of data (integers, decimals, text, etc.)
# 
# ***
# **Note:** df is short fo DataFrame, and it's a placeholder for the name given to our loaded tables. 
# ***

# In[5]:


#Changes formatting of outputed floats (#s with decimals) to show with 2 decmials and thousands separator
pd.options.display.float_format = '{:,.2f}'.format


# In[6]:


print(newDF.shape)
newDF.head() #looks good


# In[7]:


#however when we try info says object for size
newDF.info()


# Some key takeaways:
# - Most columns have 557 data points, however Issuer, Type, Size, have 558
# - Date column is being treated as "datetime64" type; this means Python is correctly treated the values as dates
# - However, the Size column should be all numbers, but the values are being treated as object (which in this case is string or text)
# 
# Another useful method to quickly check the data set is **df.tail()** which will print the last 5 rows by default (can also be given a number in brackets for more rows).

# In[8]:


newDF.tail(15)


# - It looks like after row 556, there are some blank rows, and then a "summary table" at the bottom
# - Python thinks this is part of the data set when it originally imported the table
# - We need to get rid of these extra rows at the bottom

# In[9]:


finTable = newDF.dropna()
finTable.tail()
pd.to_numeric(finTable['SIZE'])
finTable.info()


# In[10]:


finTable['SIZE'] = pd.to_numeric(finTable['SIZE'])
finTable.info()


# In[11]:


#Set the Date column as new index
finTable.set_index(['DATE'], drop=True, inplace=True)
finTable.head()


# In[12]:


finTable.index.map(lambda x: x.day)


# ## 2. Visualization and Analysis
# 
# Now that the data set is imported and clean we can start visualizing the data set and start summarizing:
# - We'll be using matplotlib and seaborn packages
# - Can create category count plots to see the count by Type/Industry/Lead Underwriter 
# - Histograms of SIZE column to see the distribution of deal sizes
# - Box Whisker plots to see distribution, outliers, average, and quartiles
# - Filters by different criteria (deals between a certain range of transaction size, deals by a particular underwrite and industry, etc.)
# - Can use **groupby** or **pivot_table** to generate summary analysis similar to Pivot Tables in Excel

# In[13]:


from matplotlib import pyplot as plt
import seaborn as sns


# In[14]:


#check num of values in each sectory category
sns.countplot(y='TYPE',data=finTable)
plt.show()


# In[15]:


finTable['INDUSTRY'].unique()


# In[16]:


#check num of values in each sectory category
fig, ax =plt.subplots(1,2, figsize=(12,5))
sns.countplot(y='INDUSTRY', data=finTable, ax=ax[0])
sns.countplot(y='LEAD UNDERWRITER', data=finTable, ax=ax[1])
fig.tight_layout()


# In[17]:


finTable.hist()
plt.show()


# In[18]:


#Box Whisker Plot by Industry
sns.boxplot(y='INDUSTRY', x='SIZE', data=finTable)
plt.show()


# In[19]:


#Box Whisker Plot by Type
sns.boxplot(y='TYPE', x='SIZE', data=finTable)
plt.show()


# <font color = 'blue'> **Filtering Data** </font>
# 
# The generic way of filtering a table is to use the following structure: dataframe[booleanMask], where the booleanMask is an IF statement type condition that creates True/False values for each row in the table.
# - The conditions can be combined using OR vs AND logic (use | for OR, use & for AND)
# 
# Below are a couple example of filtering the data.

# In[20]:


#deals between 500 and 1000
finTable[(finTable['SIZE'] >= 700) & (finTable['SIZE'] <= 1000)]


# In[21]:


#GS or MS
finTable[(finTable['LEAD UNDERWRITER'] == "Goldman Sachs") | (finTable['LEAD UNDERWRITER'] == "Morgan Stanley")]


# In[22]:


#GS Finance or MS Real Estate
finTable[((finTable['LEAD UNDERWRITER'] == "Goldman Sachs") & (finTable['INDUSTRY'] == "Finance")) |
         ((finTable['LEAD UNDERWRITER'] == "Morgan Stanley")& (finTable['INDUSTRY'] == "Real Estate"))]


# In[65]:


#Multiple filters in the same column
#Slow and Tedious
finTable[(finTable['LEAD UNDERWRITER'] == "Goldman Sachs") | (finTable['LEAD UNDERWRITER'] == "Morgan Stanley") | 
         (finTable['LEAD UNDERWRITER'] == "J.P. Morgan") | (finTable['LEAD UNDERWRITER'] == "Merrill Lynch") ]


# In[23]:


#Multiple filters in the same column
#More efficient
filter_list = ['Goldman Sachs', 'Morgan Stanley', 'J.P. Morgan', 'Merrill Lynch']
finTable[finTable['LEAD UNDERWRITER'].isin(filter_list)]


# <font color = 'blue'> **Grouping Data** </font>
# 
# Data can be aggregated using two different methods in pandas:
# - groupby
# - pivot_table --> this is closer in usage to the Pivot Tables in Excel as "values", "index" (rows) and "columns" paramaters are given (similar to dragging Fields to the Values/Rows/Columns boxes in a Pivot Table in Excel)
# 
# Below are a couple example of aggregating the data using both methods.

# In[24]:


#Groupby function
#Avg size of deals by Industry 
finTable.groupby('INDUSTRY').mean()


# In[25]:


#Sum of all deals by Type 
finTable.groupby('TYPE').sum()


# In[26]:


#Could also use .describe to summarize stats
finTable.describe()


# In[27]:


#Using Pivot Tables
pd.pivot_table(finTable, values='SIZE', index='INDUSTRY', columns='TYPE', aggfunc="sum")


# In[28]:


#Pivot Tavles with multiple Values (Size shown as Sum, Size shown as Count)
pd.pivot_table(finTable, values='SIZE', index='TYPE', aggfunc=('sum','count'))


# In[29]:


#Pivot Tavles with filters and multiple rows 
filter_list = ['Goldman Sachs', 'Morgan Stanley', 'J.P. Morgan', 'Merrill Lynch']
filteredTable = finTable[finTable['LEAD UNDERWRITER'].isin(filter_list)]
pivotDF = pd.pivot_table(filteredTable, values='SIZE', index=['LEAD UNDERWRITER','TYPE'], aggfunc=('sum','count'))
pivotDF


# In[30]:


#Exporting as Excel File
pivotDF.to_excel('../Output/Pivot Table.xlsx', sheet_name='Pivot')