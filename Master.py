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
from multiprocessing import Pool
import MetaHandler

#INSERT IMPORT MODULES HERE
from Text_Score_Module import TextScore
from bow_pdf_test import BoW_Text_Module
from page_size_ratio_module import Page_Size_Module
from scanner_detect_module import ScannerDetect
from bow_metadata import Bow_Metadata
from orientation_detector import page_orientation_module

#from ocr_bow_module import OCR_BoW_Module

def train(modules,neural_network,files,metafile):
    return

#prunes the filenames up to the point, the savefile saved the classifications last time, so the system can proceed
#instead of starting all over from the beginning
def prune(filenames, save_file):
    reader = csv.reader(save_file,delimiter=';')
    for row in reader:
        if row[0] in filenames:
            filenames.remove(row[0])
    return
    
#builds a datavector from the given list of modules.
#all modules must feature a function 'get_function(filepointer, metapointer=None)'
#which will return a single float.
#
# @param modules:   the modules extracting the features
# @return           a R^len(modules) vector (numpy-array) the datavector has the same
#                   order as the modules
def get_data_vector(file_data, metapointer=None):
    
    filepointer = open('./files/'+file_data[1]+'.pdf','rb')
    feature_data = list()
    
    for m in modules:
        try:
            #extract data-dimension from pdf
            feature_data.append(m.get_function(filepointer,metapointer))
        except:
            #if error occures the value is nan
            feature_data.append(np.nan)

    return [file_data,feature_data]

#extracts features from a set of files and returns them on a list of lists
#it also saves the features to a csv file named features.csv
#
#@param filenames:   list of filenames
#@param classes:     list of classes from the classification.csv file
#@result:            numpy array of arrays to feed the NN
#def extract_features(filenames,classes,metadata):
#        
#    c,m = get_classes(filenames,classes,metadata)
#    
#    feat_matrix = list()
#
#    for f in range(len(filenames)):
#        res=get_data_vector(modules,open(path+'/'+filenames[f],'rb'))
#        res.append(c[f])
#        res.append(filenames[f])
#        feat_matrix.append(res) 
#    
#    with open("output.csv","w") as f:
#        writer = csv.writer(f)
#        writer.writerows(feat_matrix)
#        
#    return feat_matrix
    
def extract_features(data, metadata=None):
        
    #c,m = get_classes(filenames,classes,metadata)
    
    feat_matrix = list()
    
    if p == -1:
        pool = Pool()
    else:
        pool = Pool(p)
    
    res = pool.map(get_data_vector, data)
    
    features = list()
    file_data = list()
    
    for item in res:
        features.append(item[1])
        file_data.append(item[0]) 
    
    for f, r in enumerate(features):
        r.append(file_data[f][0])
        r.append(file_data[f][1])
        feat_matrix.append(r) 
    
    with open("output.csv","w") as f:
        writer = csv.writer(f)
        writer.writerows(feat_matrix)
        
    return feat_matrix
    
#function to get the classes and metadata of the specified files
#
#@param filenames:    list of files
#@param classes:      list of classes from the classification.csv file
#@return:             list of classes (in binary) and metadata
def get_classes(filenames,classes,metadata):
    
    c = list()
    m = list()
    
    for f in filenames:
        
        #Encoding labels to make them numerical
        #There's the possibility to use categorical labels
        #by using a softmax activation algorithm on the nn
        #Could this be another way to induce a sort of bias 
        #on the different outputs by using different loss
        #functions??
        if classes[f.split('.')[0]] == True:
            c.append(1.)
        else:
            c.append(0.)
                    
        try:
            m.append(metadata[f.split('.')[0]])
        except:
            print("No metadata available for this file",f)
            
    return c,m
        
#loads the features from the csv file created during extraction
#
#@result:   list of lists of features, list of corresponding classes and filenames
def load_data(features_file):
    
    with open(features_file, 'r') as f:
      reader = csv.reader(f)
      data = list(reader)
      
    num_features = len(data[0])-2
            
    features = [item[:num_features] for item in data]

    features = generate_error_features(features)     
    
    classes = [item[num_features] for item in data]
    filenames = [item[num_features+1] for item in data]
    
    return features, classes, filenames
    
#generates the error features and replaces the nan values
#
#@result:   list of features with the error features included
def generate_error_features(features):
    
    error_feature = [0.0] * len(features)
    
    for i, x in enumerate(features):
        for j, e in enumerate(x):
            if e == 'nan':
                error_feature[i] = 1.0
                x[j] = 1.0                
    
    features = [x + [error_feature[i]] for i, x in enumerate(features)]
    return features
    
    
#function to train modules if needed. Each module called should have a train function
def train_modules(modules,filenames,classes,metadata):
    #For now modules are pre-trained
    #We want a separate function for this
    for module in modules:
        module.train(filenames,classes,metadata)
    

def get_filepointer(path,filename):
    return open(path+'/'+filename,'rb')

def get_metapointer(path):
    return MetaHandler.get_whole_metadata(path)

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
    network = NN()
    network.initializeNN(input_dim)
    return network

args = sys.argv
len_args = len(args)
training = False
extracting = False

if '-t' in args:
    training = True
    if len_args == 3:
        features_file = args[2]
    if not os.path.isfile(features_file):
        print("Error: Features file doesn't exist.")
        exit();
elif '-e' in args:
    extracting= True
    data = []
    if len_args == 3:
        data_file = args[2]
    elif len_args == 5:
        data_file = args[4]
    with open(data_file, 'r') as df:
        reader = csv.reader(df)
        data = list(reader)
    p = 1
    if args[1] == '-c':
        if args[2].isdigit():
            p = int(args[2])
        else:
            print("The -c parameter should be followed by the number of cores to be used")
            exit()

#init filepointer for save-file here, the file will contain all classifications
#maybe csv-file, not yet decided
#create file if nonexistent
if(not os.path.isfile('classes.csv')):
    with open('classes.csv', 'w') as outcsv:
        writer = csv.writer(outcsv,delimiter=';')
        writer.writerow(["Filename", "NaiveScan", "Classification"])
#open file for pruning
save_file = open('classes.csv','r')

#the threshold for the neurral Network confidence
conf_thresh = 0.5

#initialize module
modules = list()

#ADD MODULES HERE
#modules.append(TextScore(True))
#modules.append(BoW_Text_Module(True))
#modules.append(Page_Size_Module())
modules.append(ScannerDetect())
#modules.append(page_orientation_module())
#modules.append(Bow_Metadata("title"))
#modules.append(Bow_Metadata("author"))
#modules.append(Bow_Metadata("filename"))
#modules.append(Bow_Metadata("folder_name"))
#modules.append(Bow_Metadata("folder_description"))
#modules.append(Bow_Metadata("description"))

#modules.append(OCR_BoW_Module())

                
if training or extracting:
    metadata,classes = MetaHandler.get_classified_metadata("metadata.csv","classification.csv")
else:
    metadata = get_metapointer('metadata.csv')
#prune filenames if the system crashed
#prune(filenames, save_file)
#save_file.close()
#open for writing new data
#save_file = open('classes.csv','a')

#EXTRACT FEATURES HERE
if(extracting):
    print("Extracting Features from the training set. This might take a while...")
    if not data == []:
        extract_features(data, metadata)
    else:
        print("No file data provided.")

#START TRAINING HERE
if(training):
            
    features, classes, files = load_data(features_file)
        
    features = [[float(j) for j in i] for i in features]
    
    classes = [float(i) for i in classes]
    
    len_feat = len(features[0])
    
    for i in range(0, len_feat):
        max_nor=max(map(lambda x: x[i], features))
        if max_nor > 1:
            min_nor=min(map(lambda x: x[i], features))
            for f in features: (f[i] - min_nor)/(max_nor-min_nor)
    
    features=np.array([np.array(xi) for xi in features])
    
    from simple_neural_network import NN
    
    print("Initiating Neural Network")
    network = getNN(len(features[0]))
    print("Initialization finished")
    
    print("Starting training.")
    network.trainNN(features,np.array(classes))
    print("Training done!")


#classification
#batch size for the saving process
#batch_size = 10
#counter = 0
##this list will hold all classifications
#classes = list()
#for f in filenames:
#    counter += 1
#    print(str(counter)+'/'+str(len(filenames)))
#    if(counter%batch_size == 0 and not counter == 0 and batch_size != -1):
#        save_result(classes,save_file)
#        classes = list()
#    try:
#        fp = get_filepointer(path,f)
#        mp = metadata[f]
#    except:
#        print('Error opening file '+f)
#        continue
#    dat = get_data_vector(modules, fp,mp)
#    result = 0#network.predict(dat)
#
#    #interpret value of NN as confidence value
#    #the threshold serves as a adjustable bias for the classification
#    if result >= conf_thresh:
#        classes.append((f,dat,'True'))
#    else:
#        classes.append((f,dat,'False'))
#    fp.close()
#    #mp.close()
#        
#if(batch_size == -1):
#    save_result()
#save_file.close()

#ADD SOMETHING FOR PROCESSING RSUltS HERE