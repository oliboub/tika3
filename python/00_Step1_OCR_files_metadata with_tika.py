#!/usr/bin/env python
# coding: utf-8

# # test tika to convert documents in directory: category.
# - directory name of **category** of files is set in global_variables.py

# # This program intends:
# ## Step 1
# - To get multiple files in different formats, read text inside, even if it is pictures like jpog, tiff or png.<br>
# - To clean all generic words that are not necessary to define metadatas<br>
# - To generate a file with all metadatas found<br>
# 
#  |name |description|
#  |---|---|
#  | **category__metadata.csv** | list of all metadata found on existing files in the directory, containing category and filenames, count and timestamp|
#  
# 
# 

# ## Be Aware:
# in case of runing under linux ( ubuntu) and killing the process, wait that all tesseract process are finished before relaunching the python script.<br>
# The best would be to also kill the java process at the end, like it can take a lot of memory<br>

# ### Note: Hot to Convert pdf to tiff in ubuntu
# gs -o destination.tiff -r300 -sDEVICE=tiffg4 source.pdf
# gs -o eos7d-mk2-im-tiffg4-1.tiff -r200x200  -sDEVICE=tiffg4 -sPAPERSIZE=a4 -dFirstPage=2 -dLastPage=99 eos7d-mk2-im-fr.pdf

# In[ ]:


import os
from multiprocessing import Pool
from tika import parser
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


# ------
# # Functions

# ## print content of a list in multiple columns 
# Source: copy from https://stackoverflow.com/questions/1524126/how-to-print-a-list-more-nicely<br>

# In[ ]:


import math

def list_columns(obj, cols=4, columnwise=True, gap=4):
    """
    Print the given list in evenly-spaced columns.

    Parameters
    ----------
    obj : list
        The list to be printed.
    cols : int
        The number of columns in which the list should be printed.
    columnwise : bool, default=True
        If True, the items in the list will be printed column-wise.
        If False the items in the list will be printed row-wise.
    gap : int
        The number of spaces that should separate the longest column
        item/s from the next column. This is the effective spacing
        between columns based on the maximum len() of the list items.
    """

    sobj = [str(item) for item in obj]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    print(printer)


# ## Make difference between list of files (dirlist) and files already treated in the result

# In[ ]:


def diff(list1, list2):
    return list(set(list1).symmetric_difference(set(list2))) # set retire les doublons


# ## Remove non necessary words

# In[ ]:


def loop_check_stop_words(liste,word):
    a=1
    while a == 1:
        try:
            aaaa=liste.index(word)
            liste.pop(aaaa)
            if g.DEBUG_OL >= 3:
                print(liste)
        except:
            a = 0
    return(liste)


# ## Kill  java process used by tika parser to free up memory

# In[ ]:


def kill_linux_java_process():
    import psutil
    import os
    import signal

    PROCNAME = "java"
    aa=0
    bb=0
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            aa=proc.pid
            if int(aa) > int(bb):
                bb=aa
    if g.DEBUG_OL >= 3:
        print(bb)
    os.kill(bb,signal.SIGTERM)
#    time.sleep(5)


# ## Convert time in hour, minute, second

# In[ ]:


def convert_to_preferred_format(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    if g.DEBUG_OL >= 2:
        print("seconds value in hours:",hour)
        print("seconds value in minutes:",min)
    return ("%02d:%02d:%02d") % (hour, min, sec)


# ------
# # Main program
# ## Initialization

# In[ ]:


now = datetime.datetime.now()
 
if g.DEBUG_OL >= 2:
    print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

#category="doc-engineering"
#category="doc-consoles"
#category="doc-electro"
#category="doc-photo"
#category="doc-airbus"
#category="doc-tests"
dirlist = os.listdir('../'+category)
dirlist.sort()
#print(dirlist)
#for i in range(len(dirlist)):
#    dirlist[i]=''.join(dirlist[i].split())
    
if g.DEBUG_OL >= 1:
    #Display list of files formated in columns
    print(len(dirlist),' files in directory')
    list_columns(dirlist,cols=4)

##################
listDone = []                                                      # variable to retrieve all files already trated in metadata
output_directory=category+'_results'                               # directory of metadata file creation
file_lvl1=output_directory+'/'+category+'__metadata.csv'           # file name of metadata file
colonnes = ['category','file','metadata','count','timestamp']      # columns to be created in metadata file

dico = {}                                                          # temporary dictionary to create and write each line of metadata file
dico = {i : '' for i in colonnes}                                  # dictionnary initialization
##################

## collect list of files already done from dirlist
if not os.path.isdir(output_directory):
    if g.DEBUG_OL >= 2:
        print("directory does not exists. Creation launched")
    os.mkdir(output_directory)

if os.path.isfile(file_lvl1):
    reader = csv.reader(open(file_lvl1, encoding='UTF-8'))
    for row in reader:
        if row[1] not in listDone and  row[1] != 'file':
            listDone.append(row[1])
        if g.DEBUG_OL >= 2:
            print(listDone)
    if len(listDone) != len(dirlist):
        
        dirlist=diff(dirlist,listDone)

        if g.DEBUG_OL >= 1:
            #Display list of remaining files formated in columns
            print('----------------------------------------------------------')
            print(len(dirlist),'remaining files to assess:')
            list_columns(dirlist,cols=4)
            newFiles = True
    else:
        newFiles =False

if g.DEBUG_OL >= 2:
    print('newFiles:',newFiles)


# ## Request update or remove existing metadata file

# In[ ]:


if g.DEBUG_OL >= 2:
    print(file_lvl1)        
if os.path.isfile(file_lvl1):
    import PySimpleGUI as sg
    title='Selected category:'+category
    
    if newFiles == True:
        layout = [[sg.T('Do you want to remove the existing result file:',font=('Arial', 10)),
                   sg.T(file_lvl1,font=('Arial', 10, 'bold'))],
                   [sg.T('or do you prefer to add remaining/added files to the existing metadata ?',font=('Arial', 10))],
                   [sg.B('Remove',button_color=('white', 'red')), sg.B('Add',button_color=('black', 'green')), sg.T(' ',size=(40, 1)),sg.Cancel()]]
        
    elif newFiles == False:
        layout = [[sg.T('There are no new files to asses. Do you want to recreate the existing result file:',font=('Arial', 10)),
                   sg.T(file_lvl1,font=('Arial', 10, 'bold'))],
                  [sg.B('Restart and Clean metadata file',button_color=('white', 'red')), sg.T(' ',size=(40, 1)),sg.Cancel()]]
        
    window=sg.Window(title, layout)
    while True:
        events, values = window.read()
        if events == 'Cancel' or events == sg.WIN_CLOSED:
            action = 0
            exit()
            break
        elif events == 'Remove' or events == 'Restart and Clean metadata file':
            if g.DEBUG_OL >= 2:
                print(events,values)
            action = 1
            os.remove(file_lvl1)
            tableau = DataFrame(columns=colonnes)
            tableau.to_csv(file_lvl1,index=False)

            break
        elif events == 'Add':
            if g.DEBUG_OL >= 2:
                print(events,values)
            action = 2
            break
            
    if g.DEBUG_OL >= 2:
        print(action)
    window.close()

## Action sur le fichiers existants


# ------
# # prepare list of unecessary words from file

# In[ ]:


#STOP_WORDS_FILE="stop_words_french.txt"
#STOP_WORDS_FILE="stop_words_english.txt"
STOP_WORDS_FILE="stop_fr_en_words.txt"

with open(STOP_WORDS_FILE, 'r', encoding='UTF-8') as file:
    stop_words = file.read().splitlines()

if g.DEBUG_OL >= 3:
    print(stop_words)


# ## Main process to treat tika ocr in files

# In[ ]:


def traiteocr(dirlist):
   
    liste =[]
    str_match=[]
#    print("-----------------------\n",dirlist)
    abspath = '../'+category
#    print(abspath)
    full_dir=os.path.abspath(abspath)
#    print(full_dir)
    aa=full_dir+'/'+dirlist
    inode=os.stat(aa).st_ino
#    print(full_dir+'/'+i," en cours...")

    collectedtime = datetime.datetime.now()
    if g.DEBUG_OL >= 2:
        print(collectedtime)
    
    parsed_file = parser.from_file(aa,requestOptions=({'timeout': 1000}))
    time.sleep(1)
    my_metadata=parsed_file['metadata']
    my_content = parsed_file['content']
    if g.DEBUG_OL >= 2:
#        print('my_metadata:',my_metadata)
        print('my_content:',my_content)
       
    result = re.sub('[^A-Za-z0-9°éèàçùïœæ]+', ' ', my_content)
    result = result.replace('\n', '').lower()    


    if g.DEBUG_OL >= 2:
        print('result:',result)
    liste = result.split()
    
    if g.DEBUG_OL >= 2:
        print('\n----------------------------------\n----->liste brute:',liste)

    for h in stop_words:
        try:
            liste=loop_check_stop_words(liste,h)
        except:
            pass

    if g.DEBUG_OL >= 2:
        print('\n----------------------------------\n----->liste_stop_words:',liste)
 
    counts = Counter(liste)
    if g.DEBUG_OL >= 2:
        print('\n----------------------------------\n----->counts:',counts)
    with open(file_lvl1,'a',encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames = colonnes,lineterminator='\n')
        for cle, valeur in counts.items():
            if g.DEBUG_OL >= 2:
                print(dirlist,cle, valeur)
            dico['category'] = category
            dico['file'] = dirlist
            dico['metadata']=str(cle)
            dico['count']=int(valeur)
            dico['timestamp'] = collectedtime
            writer.writerow(dico)
        if g.DEBUG_OL >= 1:
            print(dirlist,' Done...')


# In[ ]:


if __name__ == "__main__":
    start_func_time = time.time()
    print("Launching...\n Be patient...")
    print('Collection of metadata in ',len(dirlist),' files')
    with Pool (g.parallel) as p:
        p.map(traiteocr,dirlist)
    curr_time = time.time() - start_func_time
    returned_time=convert_to_preferred_format(curr_time)
    print('Process finished in,',returned_time[0:2],'heure(s)',returned_time[3:5],'minute(s)',returned_time[6:8],'seconds' )


# In[ ]:


time.sleep(5)
if platform == "linux" or platform == "linux2":
    check_call(['sync'])
    kill_linux_java_process()


# In[ ]:




