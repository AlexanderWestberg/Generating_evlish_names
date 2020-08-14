import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    
 
    
'''
First Data is from Thoughtcatalog
'''    

   
herinterest_url = "https://thoughtcatalog.com/january-nelson/2018/06/elf-names/"

herinterest_pageTree = requests.get(herinterest_url, headers=headers)

herinterest_pageSoup = BeautifulSoup(herinterest_pageTree.content, 'html.parser')

herinterest = herinterest_pageSoup.find_all("p")


herinterest_list = []
len_herinterest = len(herinterest)

for a in range(0,len_herinterest):
    herinterest_list.append(herinterest[a].text)



herinterest_list = herinterest_list[5:907]


df_herinterest = pd.DataFrame(herinterest_list)
df_herinterest.columns =["Elvish_Names"]

'''
Second data is from arwen

-
'''

 
arwen_girls_url = "http://www.arwen-undomiel.com/elvish/girlnames.html"

arwen_girls_pageTree = requests.get(arwen_girls_url, headers=headers)

arwen_girls_pageSoup = BeautifulSoup(arwen_girls_pageTree.content, 'html.parser')

arwen_girls_interest = arwen_girls_pageSoup.find_all("b")


arwen_girls_list = []
len_arwen_girls_interest = len(arwen_girls_interest)


for i in range(1, len_arwen_girls_interest):
    import re
    
    name = re.search(r"<b>(.*)<br/>", str(arwen_girls_interest[i].parent))
    
    if type(name) == re.Match:
        
        name = name.group(0).replace("<b>","").replace("<br/>", "")
    
        if "(" in name:
            name = name[:name.find("(")-1]
                            
        if "<i>" in name:
            name = name[:name.find("<i>")-1]
        
        if "</b>" in name:
            name = name[:name.find("</b>")]
            
                        
        arwen_girls_list.append(name)
arwen_girls_list.pop(587)    
arwen_girls_list.pop(724)       
        

    


df_arwen_girls = pd.DataFrame(arwen_girls_list)
df_arwen_girls.columns =["Elvish_Names"]


'''
The third datasource

'''

  
arwen_boys_url = "http://www.arwen-undomiel.com/elvish/boynames.html"

arwen_boys_pageTree = requests.get(arwen_boys_url, headers=headers)

arwen_boys_pageSoup = BeautifulSoup(arwen_boys_pageTree.content, 'html.parser')

arwen_boys_interest = arwen_boys_pageSoup.find_all("b")


arwen_boys_list = []
len_arwen_boys_interest = len(arwen_boys_interest)


for i in range(1, len_arwen_boys_interest):
    import re
    
    name = re.search(r"<b>(.*)<br/>", str(arwen_boys_interest[i].parent))
    
    if type(name) == re.Match:
        
        name = name.group(0).replace("<b>","").replace("<br/>", "")
    
        if "(" in name:
            name = name[:name.find("(")-1]
                            
        if "<i>" in name:
            name = name[:name.find("<i>")-1]
        
        if "</b>" in name:
            name = name[:name.find("</b>")]
            
                        
        arwen_boys_list.append(name)



df_arwen_boys = pd.DataFrame(arwen_boys_list)
df_arwen_boys.columns =["Elvish_Names"]



'''
This is where we combine all the data into 1 file

'''

df_merge = pd.concat([df_arwen_boys, df_arwen_girls, df_herinterest])


df_merge.to_csv("All_Elvish_Names")
