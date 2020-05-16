#!/Users/simon/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Covid-19</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Simon Ramirez Hinestrosa</bitbar.author>
# <bitbar.author.github>your-github-username</bitbar.author.github>
# <bitbar.desc>Tracks the covid-19 numbers from https://www.worldometers.info/coronavirus/</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>
"""
Created on Sun Apr  5 11:51:27 2020

Code based on:
https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059
@author: simon
"""

import requests
import lxml.html as lh
import pandas as pd
import numpy as np




def get_main_table(url):
    
    """
    Gets a table from url 
    
    Args:
        url of the website containing the table
    
    Return:
        df pandas dataframe
    """


    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    
    
    # =============================================================================
    # Getting the header
    # =============================================================================
    # parse the first row as our header.
    tr_elements = doc.xpath('//tr')
    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))
        
        
    # =============================================================================
    # Creating Pandas data frame
    # =============================================================================
        
    
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
    #    #If row is not of size 10, the //tr data is not from our table 
    #    if len(T)!=10:
    #        break
    #    
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
            
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    
    return df

def longest_per_column(table, header):
    """
    returns the length of the longest string in the column
    """
    
    total = []
    for i,name in enumerate(header):
        lengths = []
        column = table[:,i]
        for row in column:
            lengths.append(len(str(row)))
            lengths.append(len(name))
        
        total.append(np.max(lengths))
        
    return total


df = get_main_table('https://www.worldometers.info/coronavirus/')
header =['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths']


# Dummy column to sort
df['TotalCases'] = df['TotalCases'].astype(str) # to be able to use next line
df['sort_column'] = df['TotalCases'].str.replace(',','', regex=True)


# Drop rows with "Total:" in the first column
#index_total = df[ df[header[1]] == "Total:" ].index
#df.drop(index_total , inplace = True)

#index_empty = df[ df[header[0]] == " " ].index
#df.drop(index_empty , inplace = True)


table_continents = df.values[:6]
table = df.values[7:]



#TODO df has twice the same table, check the tr_elements
column_country = df.columns.get_loc('Country,Other')

index = np.where(table == header[0])[0][0]  # The table repeats itself here
index_total = np.where(table[:,column_country]=='Total:') # continents have that colum with "Total:"
index = np.min(index_total)
table = table[:index,:]
table[:,-1] = table[:,-1].astype(float)

df2 = pd.DataFrame(table, columns = df.columns )
df3 = pd.DataFrame(table_continents)


# Sorting the table based on the total cases
table = table[table[:,-1].argsort()][::-1]

# Working on the top 10
lengths = longest_per_column(table[:11,1:5],header)

# Target country to track

target_country = 'Colombia'
ind_target = np.where(table[:,column_country] == target_country)[0][0]

print ("\u001b[1m C-19\n") 
print("---")
# Getting the longest string 
print(f"{header[0]:<{lengths[0]}}\t{header[1]:<{lengths[1]}}\t\t{header[2]:<{lengths[2]}}\t\t{header[3]:<{lengths[3]}} | color=black")  
print("---")
print (f"{table[0][0]:<{lengths[0]}}\t\t{table[0][1]:<{lengths[1]}}\t\t{table[0][2]:<{lengths[2]}}\t\t{table[0][3]:<{lengths[3]}} | color=black ")

#print (f"{table_continents[0][0]:<{lengths[0]}}\t\t{table_continents[0][1]:<{lengths[1]}}\t\t{table_continents[0][2]:<{lengths[2]}}\t\t{table[0][3]:<{lengths[3]}} | color=black ")

print("---")
for i in range(1,11):
    print (f"{table[i][0]:<{lengths[0]}}\t\t{table[i][1]:<{lengths[1]}}\t\t{table[i][2]:<{lengths[2]}}\t\t\t{table[i][3]:<{lengths[3]}}") 

print("---")
i = ind_target
print (f"{table[i][0]:<{lengths[0]}}\t\t{table[i][1]:<{lengths[1]}}\t\t{table[i][2]:<{lengths[2]}}\t\t\t{table[i][3]:<{lengths[3]}}| color=orange")
