#!/Users/simon/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-
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
header = df.columns[:4]


# Dummy column to sort
df[header[1]] = df[header[1]].astype(str) # to be able to use next line
df['sort_column'] = df[header[1]].str.replace(',','', regex=True)

table = df.values



#TODO df has twice the same table, check the tr_elements
index = np.where(table == header[0])[0][0]  # The table repeats itself here
table = table[:index,:]
table[:,-1] = table[:,-1].astype(float)

df2 = pd.DataFrame(table)

# Sorting the table based on the total cases
table = table[table[:,-1].argsort()][::-1]

# Working on the top 10
lengths = longest_per_column(table[:11,:4],header)



print ("\u001b[1m C-19\n") #http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
print("---")
# Getting the longest string 
print(f"{header[0]:<{lengths[0]}}\t{header[1]:<{lengths[1]}}\t\t{header[2]:<{lengths[2]}}\t\t{header[3]:<{lengths[3]}}")  #https://stackoverflow.com/questions/8234445/python-format-output-string-right-alignment
print (f"{table[1][0]:<{lengths[0]}}\t\t{table[1][1]:<{lengths[1]}}\t\t{table[1][2]:<{lengths[2]}}\t\t{table[1][3]:<{lengths[3]}}")
print("---")
for i in range(2,11):
    print (f"{table[i][0]:<{lengths[0]}}\t\t{table[i][1]:<{lengths[1]}}\t\t{table[i][2]:<{lengths[2]}}\t\t{table[i][3]:<{lengths[3]}}") #https://realpython.com/python-f-strings/

