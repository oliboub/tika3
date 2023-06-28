# <span style="color:orange">README.md</span>

## <span style="color:blue">Introduction</span>
This git is used to try apache tika on different documents format.<br>
the aim is to collect all words, out of stopwords, in the content of the documents and create files with metadata.<br>
After, you can search or draw treemap or wordclouds based on the csv generated.<br>

stopwords can be changed to other language, just check on this site:
https://countwordsfree.com/stopwords/french

Drawings are based on this information:
https://towardsdatascience.com/beyond-the-cloud-4-visualizations-to-use-instead-of-word-cloud-960dd516f215

wordcloud tutorial:
https://www.youtube.com/watch?v=l7w7unBNAeU

a category is needed. it means a subdirectory of the home directory with your all your documents (images, documents) files to be transformed in textual words.<br>
category is defined in the file: **python/global_variables.py** (it can be moved directly in the directory jupyter_files if needed)<br>

<br>
<u>New in this version tika3:</u><br>
- Change way of working by using dictionnary and parallelisation. Increase speed a lot.<br>
     > parallel parameter can be found in global_variables.py<br>
 - Simplification.<br>
- pysimplegui interface to chose remove or add data into file<br>
- compare files treated in the result file to be able to retrieve in case of missing or added new files<br>

Change has been done following a training in Udemy: "Python Coder un dashboard de Rachid." It seems that this training is not yet opened for trainnee..<br>
<br>

## <span style="color:blue">Files usage </span>
1 file is already developped,
| FIle | Description |
| --- | --- |
| jupyter_files/**00_Step1_OCR_files_metadata with_tika.ipynb** | tika parsing of files from a category directory, with output is a file with all metadata found, including  qtt by file  |


## <span style="color:blue">result </span>
Results wil be provided in a subdirectory named: *category*_results
| FIle | Description |
| --- | --- |
| category__metadatas.csv | file with all treated files with data format as :  ['category','file','metadata','count','timestamp'] |

## <span style="color:blue">Development environment</span>
- using ubuntu 23 with python 3.11 and openjava sdk 17<br>
- using jupyter lab<br>
- working in a venv (virtual environment)<br>
- To use jupyter files, you need to add the subdirectory **python** in the PYTHONPATH variable. it is where is located the global_variables.py<br>

- for tika, java jdk is needed


## <span style="color:blue">additional libraries used</span>
to be added in the vitrual environment with pip.<br>
- **tika**<br>
- **jupyterlab**<br>
- **pandas**<br>
- **pysimplegui**<br>
<br>
 
## <span style="color:blue">log mod</span>
to change the log level and get more print:<br>
- change **DEBUG_OL** value to **2** in the file ./python/global_variables.py<br>

## <span style="color:blue">debug mode</span>
to check function or different steps of the code, it can be done inside jupyter lab, by executing some steps and creating to launch unitary tests.<br>

## backlog and issues
Local follow-up is in the file:<br>
[backlog & issues](./todo_list.md)