__author__ = 'matsrichter'

import time
import page_size_ratio_module as pgr
import bow_pdf_test as bow
import Text_Score_Module as ts
import scanner_detect_module as sm
import csv
import os
import MetaHandler as mh

def get_files():
    filenames = list()
    file_class = list()

    #create dictionary with classifications
    with open('classification.csv','rb') as classes:
        c = 0
        reader = csv.reader(classes,delimiter=';', quotechar='|')
        first = True
        for row in reader:
            if first:
                first = False
                continue
            c += 1
            if c == 101:
                break
            #file_class['testdata/'+row[0]+'.pdf'] = row[2]
            file_class.append(row[2])
            filenames.append('./files/'+row[0]+'.pdf')
    mp = mh.get_whole_metadata('metadata.csv')
    return filenames, file_class,file_class

def test_performance(fp,meta,classes,module,module_name):
    start = time.time()
    if(module_name == 'Scan-Detect:'):
        module.train('./files','classification.csv')
    else:
        #   testung size_ratio
        module.train(fp,meta,classes)
    end = time.time()
    return module_name +":\t"+ str(end-start)



fp, meta,classes = get_files()
#scan_detect = sm.ScannerDetect()
size_ratio = pgr.Page_Size_Module()
txt_score = ts.TextScore()
bow_txt = bow.BoW_Text_Module('full',txt_score)
print('start testing...')
result = list()
#result.append(test_performance(fp,meta,classes,scan_detect,'Scan-Detect'))
print("1/4")
result.append(test_performance(fp,meta,classes,size_ratio,'Page/Size-Ratio'))
print("2/4")
result.append(test_performance(fp,meta,classes,bow_txt,'BoW-Text-Score'))
print("3/4")
result.append(test_performance(fp,meta,classes,txt_score,'Textlength'))
print("4/4")
print('')
print('Final Results:')
for r in result:
    print(r)
