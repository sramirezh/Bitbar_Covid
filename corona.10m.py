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


table = get_main_table('https://www.worldometers.info/coronavirus/')
np_table = table.values

print ('%s %s'%(np_table[0][0],np_table[0][1]))
