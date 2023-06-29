#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys
from multiprocessing import Pool
import datetime
import pandas as pd
from pandas import DataFrame
import re
import time
import psutil
import os  
from subprocess import check_call
import signal
from sys import platform
from collections import Counter
import csv

#print(platform)

start_time = time.time()


# In[ ]:


import global_variables as g
g.init()

category=g.category


# # Init category and files

# In[ ]:


##################
listDone = []                                                      # variable to retrieve all files already treated in metadata
output_directory=category+'_results'                               # directory of metadata file creation
file_lvl1=output_directory+'/'+category+'__metadata.csv'           # file name of metadata file
file_wordcloud = output_directory+'/'+category+'__wordcloud1.png'  # file name of first wordcloud image

colonnes = ['category','file','metadata','count','timestamp']      # columns to be created in metadata file

dico = {}                                                          # temporary dictionary to create and write each line of metadata file
dico = {i : '' for i in colonnes}                                  # dictionnary initialization
##################


# ## Prepare list of remaining files

# In[ ]:


import re
listDone = []
reader = ''
if g.DEBUG_OL >= 2:
    print('output_directory',output_directory,'\tfile_lvl1:',file_lvl1)
    
if not os.path.isdir(output_directory):
    if g.DEBUG_OL >= 2:
        print("directory does not exists")
    sys.exit()

if os.path.isfile(file_lvl1):
    if g.DEBUG_OL >= 2:
        print('ok')
    reader = csv.reader(open(file_lvl1, encoding='UTF-8'))
    for row in reader:
        if not re.match(r'[0-9]',row[2]):
#            print(row[2])
            listDone.append(row[2])
#    listDone.sort()
    if g.DEBUG_OL >= 2:
        print('\nlen(listDone):',len(listDone) ,'\tlistDone',listDone[10:50])

else:
    if g.DEBUG_OL >= 2:
        print("File does not exist")
    sys.exit()


# In[ ]:


listWords = '\n'.join(map(str, listDone))
type(listWords)
if g.DEBUG_OL >= 2:
    print(len(listWords))


# In[ ]:


from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

width =1600
height=900

MY_DPI = 96 # (site: https://fr.infobyip.com/detectmonitordpi.php)
wc = WordCloud(
    width =width,
    height=height,
    margin=10,
#    max_font_size=20,
    max_words=100,
    collocations=False,
    repeat=False,

).generate(listWords)


# In[ ]:


plt.figure(figsize=(width/MY_DPI,height/MY_DPI))
plt.imshow(wc,interpolation='bilinear')
plt.axis('off') # enleve les axes
plt.margins(x=0, y=0)
plt.savefig(file_wordcloud, dpi=MY_DPI)


# In[ ]:




