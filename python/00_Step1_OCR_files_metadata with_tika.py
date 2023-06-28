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

# ----------
# # Import modules

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


# # Init category and files

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
    print(len(dirlist),' files in directory\n')
    
#print(dirlist)
#ii=0


# ------
# # Functions

# ## Format lists as columns for display in pysimplegui table

# In[ ]:


def formatcol(liste,displayedCol=4):
    liste2Print = []
    cc=[]
    
    displayedColLen = len(liste)//displayedCol
    displayedColModulo = len(liste)%displayedCol
    if g.DEBUG_OL >= 3:
        print('displayedCol:',displayedCol,'\tdisplayedColLen:',displayedColLen,'\tdisplayedColModulo:',displayedColModulo)
    for i in range(displayedColLen):
    #    print(dirlist[::displayedCol][i], '\t' ,dirlist[1::3][i], '\t' ,dirlist[2::3][i],'\t',dirlist[3::displayedCol][i])
        cc = [liste[::displayedCol][i], liste[1::3][i], liste[2::3][i],liste[3::4][i]]
        liste2Print.append(cc)
        
    for j in range(displayedColModulo):
        if j == 0:
    #        print(dirlist[::displayedCol][displayedColLen])
            aa = liste[::displayedCol][displayedColLen]
            cc=[aa]
    
        elif j == 1:
    #        print(dirlist[1::3][displayedColLen])
            bb= liste[1::3][displayedColLen]
            cc=[aa,bb]
    
        elif j == 2:
    #        print(dirlist[2::3][displayedColLen])
            dd= liste[2::3][displayedColLen]
            cc=[aa,bb,dd]
    
            
    liste2Print.append(cc)
    
    if g.DEBUG_OL >= 3:
        print(len(liste2Print),liste2Print)
    return liste2Print


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


# ## Main function to treat tika ocr in files

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


# ------
# # Main program
# ## Initialization

# In[ ]:


##################
listDone = []                                                      # variable to retrieve all files already trated in metadata
output_directory=category+'_results'                               # directory of metadata file creation
file_lvl1=output_directory+'/'+category+'__metadata.csv'           # file name of metadata file
colonnes = ['category','file','metadata','count','timestamp']      # columns to be created in metadata file

dico = {}                                                          # temporary dictionary to create and write each line of metadata file
dico = {i : '' for i in colonnes}                                  # dictionnary initialization
##################


# ## Prepare list of remaining files

# In[ ]:


remainList = []
if g.DEBUG_OL >= 2:
    print('output_directory',output_directory,'\tfile_lvl1:',file_lvl1)
if not os.path.isdir(output_directory):
    if g.DEBUG_OL >= 2:
        print("directory does not exists. Creation launched")
    os.mkdir(output_directory)

if os.path.isfile(file_lvl1):
    fileExists=True
    reader = csv.reader(open(file_lvl1, encoding='UTF-8'))
    for row in reader:
        if row[1] not in listDone and  row[1] != 'file':
            listDone.append(row[1])
        if g.DEBUG_OL >= 2:
            print(listDone)
    if len(listDone) != len(dirlist):
        
        remainList=diff(dirlist,listDone)
        newFiles = True
        
        if g.DEBUG_OL >= 2:
            #Display list of remaining files formated in columns
            print('----------------------------------------------------------')
            print(len(remainList),'remaining files to assess:')
            
    else:
        newFiles =False

    if g.DEBUG_OL >= 2:
        print('newFiles:',newFiles)
else:
    fileExists=False

if g.DEBUG_OL >= 2:
    print('fileExists:',fileExists)
    print('end process: Prepare list of remaining files')


# ## Create displayable list of all files in pysimplegui

# In[ ]:


fullListe2Print = formatcol(dirlist)


# ## Create displayable list of remaining files in pysimplegui

# In[ ]:


if fileExists == True:
    remainListe2Print = formatcol(remainList)


# ## Display full files list and remaining files list and request action

# In[ ]:


if fileExists == True:
    import PySimpleGUI as sg
    title="Analyze of files to treat"
    
    layout = [[sg.T(len(dirlist),font=('Arial', 10, 'bold'), text_color='yellow'),sg.T('files found in the directory',font=('Arial', 10)),sg.T(output_directory,font=('Arial', 10, 'bold'), text_color='yellow'),sg.T(' ',size=(40, 1)),sg.T('Parallelization:',font=('Arial', 10)),sg.T(g.parallel,font=('Arial', 10, 'bold'), text_color='yellow') ],
              [sg.Table(fullListe2Print,auto_size_columns=True,display_row_numbers=False,header_text_color='white on blue',selected_row_colors='white on blue',justification='left',expand_x=True,expand_y=True,)],
              [sg.T(len(remainList),font=('Arial', 10, 'bold'), text_color='lightgreen'),sg.T('remaining files to assess',font=('Arial', 10)) ],
              [sg.Table(remainListe2Print,auto_size_columns=True,display_row_numbers=False,header_text_color='white on blue',selected_row_colors='white on blue',justification='left',expand_x=True,expand_y=True,)],[sg.T(' ',size=(40, 1))]]
    
    if newFiles == True:
        laycase = [[sg.T('Do you want to remove the existing result file:',font=('Arial', 10)),
                   sg.T(file_lvl1,font=('Arial', 10, 'bold'), text_color='yellow')],
                  [sg.T('or do you prefer to add remaining/added files to the existing metadata ?',font=('Arial', 10))]
                  ,[sg.B('Remove',button_color=('white', 'red')), sg.B('Add',button_color=('black', 'green')), sg.T(' ',size=(40, 1)),sg.Cancel()]]
        
    elif newFiles == False:
        laycase = [[sg.T('There are no new files to asses. Do you want to recreate the existing result file:',font=('Arial', 10)),
                   sg.T(file_lvl1,font=('Arial', 10, 'bold'), text_color='yellow')],
                  [sg.B('Restart and Clean metadata file',button_color=('white', 'red')), sg.T(' ',size=(40, 1)),sg.Cancel()]]
    
    layout.append(laycase)
    
    window=sg.Window(title, layout, resizable=True)
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
            dirlist = remainList
            action = 2
            break
            
    if g.DEBUG_OL >= 2:
        print(action)
    window.close()
if g.DEBUG_OL >= 2:
    print('end process: Display full files list and remaining files list and request action (pysimplegui)')


# ## prepare list of unecessary words from file

# In[ ]:


#STOP_WORDS_FILE="stop_words_french.txt"
#STOP_WORDS_FILE="stop_words_english.txt"
STOP_WORDS_FILE="stop_fr_en_ge_sp_words.txt"

with open(STOP_WORDS_FILE, 'r', encoding='UTF-8') as file:
    stop_words = file.read().splitlines()

if g.DEBUG_OL >= 3:
    print(stop_words)


# ------
# # Init process

# In[ ]:


if __name__ == "__main__":
    start_func_time = time.time()
    print("Launching...\n Be patient...")
    print('Collection of metadata in ',len(dirlist),' file(s)')
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




