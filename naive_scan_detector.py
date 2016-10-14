__author__ = 'matsrichter'

"""
This scanner detector uses a textline handed over by the BoW module for text
extraction or extracts the text by itself and checks if the given string has length of one.
If so, the file is most likely a scan. When this is not the case.
"""

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

class Naive_Scan_Detector:

    def __init__(self,txt_module = None):
        """

        :param txt_module: a text-score module, this module must be called first
        :return:
        """
        self.error = False
        self.text_module = txt_module
        return

    # @param pages number of pages to transform to text starting from the first
    # if the argument is set to -1, all pages are read
    # @return a utf-8 coded string from the pdf.
    def convert_pdf_to_txt(self,fp,pages=-1):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            if(pages==0):
                break
            interpreter.process_page(page)
            pages -= 1

        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        #print(len(text))
        print(int(raw_input(text[0])))
        return len(text)

    def get_function(self,filepointer, metapointer = None):

        if(self.text_module == None or True):
            result = len(self.convert_pdf_to_txt(filepointer))
        else:
            result = len(self.text_module.x)
        print result
        try:
            if(result > 1):
                return 0.0
            else:
                #print("HIT")
                return 1.0
        except:
            self.error = True
            return 0.5

    def train(self,filenames,classes,metalist = None):
         return