# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:16:02 2016

This will be the main executing script of the system
This script is extended as the system grows

@author: Mats L. Richter
"""
import csv
import numpy as np
import os, os.path, sys

#INSERT IMPORT MODULES HERE
from Text_Score_Module import TextScore
from bow_pdf_test import BoW_Text_Module
from page_size_ratio_module import Page_Size_Module

#INSERT IMPORT OF NEURAL NETWORK HERE

#prunes the filenames up to the point, the savefile saved the classifications last time, so the system can proceed
#instead of starting all over from the beginning
def prune(filenames, save_file):
    reader = csv.reader(save_file,delimiter=';')
    for row in reader:
        if row[0] in filenames:
            filenames.remove(row[0])
    return

#get all filenames
#the system currently assumes that all pdfs are stored in a single folder
#simply called 'files'
def get_files(path='./files'):
    filenames = list()
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            filenames.append(file)
    return filenames
    
#builds a datavector from the given list of modules.
#all modules must feature a function 'get_function(filepointer, metapointer=None)'
#which will return a single float.
#
# @param modules:   the modules extracting the features
# @return           a R^len(modules) vector (numpy-array) the datavector has the same
#                   order as the modules
def get_data_vector(modules, filepointer, metapointer=None):
    data = list()
    for m in modules:
        try:
            #extract data-dimension from pdf
            data.append(m.get_function(filepointer,metapointer))
        except:
            #if error occures the value is 0.0
            data.append(0.0)
    #return as numpy array
    return np.array(data)

def get_filepointer(path,filename):
    return open(path+'/'+filename,'r')

def get_metapointer(path,filename):
    return

def save_result(classes, save_file):
    """
    @input classes: the saved data as a list of 3-tuples
                    (filename, data_vector, classification)
    @return:        True if saves succesfully
    """
    for data in classes:
        save_string = data[0]+';'
        for d in data[1]:
            save_string = save_string+str(d)+';'
        save_string = save_string + data[2]
        save_file.write(save_string+"\n")
        save_file.flush()
    return True

#this function will initialize the neural network
# @parram input_dim:    number of modules for the input vector
def getNN(input_dim):
    return


#init filepointer for save-file here, the file will contain all classifications
#maybe csv-file, not yet decided
#create file if nonexistent
if(not os.path.isfile('classes.csv')):
    with open('classes.csv', 'wb') as outcsv:
        writer = csv.writer(outcsv,delimiter=';')
        writer.writerow(["Filename", "TextScore","BoWTextScore","Pagesize(KBytes)", "Classification"])
#open file for pruning
save_file = open('classes.csv','r')

#the threshold for the neurral Network confidence
conf_thresh = 0.5

#initialize module
modules = list()
modules.append(TextScore())
modules.append(BoW_Text_Module())
modules.append(Page_Size_Module())

#init neural network
network = getNN(len(modules))

#get filenames
path = './files'
filenames = get_files(path)
#prune filenames if the system crashed
prune(filenames, save_file)
save_file.close()
#open for writing new data
save_file = open('classes.csv','a')


#classification
#batch size for the saving process
batch_size = 10
counter = 0
#this list will hold all classifications
classes = list()
for f in filenames:
    counter += 1
    print(str(counter)+'/'+str(len(filenames)))
    if(counter%batch_size == 0 and not counter == 0 and batch_size != -1):
        save_result(classes,save_file)
        classes = list()
    try:
        fp = get_filepointer(path,f)
        mp = get_metapointer(path,f)
    except:
        print('Error opening file '+f)
        continue
    dat = get_data_vector(modules, fp,mp)
    result = 0#network.predict(dat)

    #interpret value of NN as confidence value
    #the threshold serves as a adjustable bias for the classification
    if result >= conf_thresh:
        classes.append((f,dat,'True'))
    else:
        classes.append((f,dat,'False'))
    fp.close()
    #mp.close()
        
if(batch_size == -1):
    save_result()
save_file.close()
