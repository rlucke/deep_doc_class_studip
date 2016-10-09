__author__ = 'matsrichter'

import time
import page_size_ratio_module as pgr
import bow_pdf_test as bow
import Text_Score_Module as ts
import scanner_detect_module as sm
import MetaHandler as mh

def get_files():
    return list(), list(),list()

def test_performance(fp,meta,classes,module,module_name):
    start = time.time()
    #   testung size_ratio
    module.train(fp,meta,classes)
    end = time.time()
    return module_name +":\t"+ str(end-start)



fp, meta,classes = get_files()

size_ratio = pgr.Page_Size_Module()
bow_txt = bow.BoW_Text_Module()
txt_score = ts.TextScore()
scan_detect = sm.ScannerDetect()
print('start testing...')
result = list()
print("1/4")
result.append(test_performance(fp,meta,classes,size_ratio,'Page/Size-Ratio:'))
print("2/4")
result.append(test_performance(fp,meta,classes,bow_txt,'BoW-Text-Score'))
print("3/4")
result.append(test_performance(fp,meta,classes,txt_score,'Textlength:'))
print("4/4")
result.append(test_performance(fp,meta,classes,scan_detect,'Scan-Detect:'))
print()
print('Final Results:')
for r in result:
    print(r)
