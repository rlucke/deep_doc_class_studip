# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 12:16:02 2016

This will be the main executing script of the system
This script is extended as the system grows

@author: Mats L. Richter
"""
import numpy as np
import os, os.path, sys

#INSERT IMPORT MODULES HERE
from Text_Score_Module import TextScore

#INSERT IMPORT OF NEURAL NETWORK HERE

#prunes the filenames up to the point, the savefile saved the classifications last time, so the system can proceed
#instead of starting all over from the beginning
def prune(filenames, save_file):
    return

#get all filenames
#the system currently assumes that all pdfs are stored in a single folder
#simply calles 'files'
def get_files(path='./files'):
    filenames = list()
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            filenames.append(file)
    return filenames
    
#builds a datavector from the given list of modules.
#all modules must feature a function 'get_function(filepointer, metapointer=None)'
#which will return a single float.
#@parram modules: the modules extracting the features
#@return a R^len(modules) vector (numpy-array) the datavector has the same 
# order as the modules
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
    return open(path+filename,'r')

def get_metapointer(path,filename):
    return

#save the file in a save file
#@param result the list with classification
#@parram filenames the name of the classified files, same order as result
#@param batch_size: the latest batch_size results are written in the file
# -1 indicates that the batchsize is equal to the total number of files to
# classify
# saves also the data-vector
#give csv rows names
def save_result(result,filenames,save_file, batch_size = -1):
    return

#this function will initialize the neural network
#@parram input_dim: number of modules for the input vector
def get_NN(input_dim):
    return


#init filepointer for save-file here, the file will contain all classifications
#maybe csv-file, not yet decided
save_file = None

#the threshold for the neurral Network confidence
conf_thresh = 0.5

#initialize module
modules = list()
modules.append(TextScore())

#init neural network
network = getNN(len(modules))

#get filenames
path = './files'
filenames = get_files(path)
#prune filenames if the system crashed
prune(filenames, save_file)

#classification
#batch size for the saving process
batch_size = 100
counter = 0
#this list will hold all classifications
classes = list()
for f in filenames:
    counter += 1
    if(counter%batch_size == 0 and not counter == 0 and batch_size != -1):
        save_result(classes, save_file, batch_size)
    try:
        fp = get_filepointer(path,f)
        mp = get_metapointer(path,f)
    except:
        print('Error opening file '+f)
        continue
    result = network.predict(get_data_vector(modules, fp,mp))
    #interpret value of NN as confidence value
    #the threshold serves as a adjustable bias for the classification
    if result >= conf_thresh:
        classes.append('True')
    else:
        classes.append('False')
    fp.close()
    mp.close()
        
if(batch_size = -1):
    save_result(classes, filenames, save_file, -1)
save_file.close()
