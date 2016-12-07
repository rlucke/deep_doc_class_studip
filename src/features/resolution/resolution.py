__author__ = 'matsrichter'

from os.path import join, realpath, dirname, isdir, basename
MOD_PATH = dirname(realpath(__file__))
from doc_globals import*
from PyPDF2 import PdfFileReader
import numpy as np

class Resolution_Module:

    def __init__(self, side = 'x'):
        """

        :param side: 'x' - measure the x-axis in pixels
                     'y' - measure the y-axis  in pixels
        """
        self.side = side
        self.name = ['resolution']
        self.error = False

    def get_function(self,fp, metapointer = None):
        try:
            pdf = PdfFileReader(fp)
            page = pdf.getPage(0).mediaBox
            if(self.side == 'x'):
                return np.float64(page.getUpperRight_x() - page.getLowerLeft_x())
            else:
                return np.float64(page.getUpperRight_y() - page.getLowerRight_y())
        except:
            self.error = True
            return np.float64(0.0)



    def train(self,filenames,classes,metalist = None):
        return