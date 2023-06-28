#!/usr/bin/env python
# coding: utf-8

# # global_variables

# In[ ]:


import os

def init():
    global DEBUG_OL
    DEBUG_OL=1

    # DEBUG_OL
    # 0 means no print
    # 1 means print call to function only
    # 2 means print all
    # 3 is to add functions log in the global log
    # -1 Special cases

    global parallel
    parallel = 4
    
    global FONT
    FONT='Helvetica 11'
    
    global THEME
    THEME = 'LightBlue2'
    
    global category
    #category="doc-engineering"
    #category="doc-consoles"
    #category="doc-electro"
    category="doc-photo"
    #category="doc-airbus"
    #category="doc-tests"
    #category="doc-tiff"
