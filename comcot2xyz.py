'''
This code is used to convert comcot output from each layer into XYZ file either 
for zmax (inundation), or ETA. the output will be layer{LN}_x.dat for longitude,
layer{LN}_y.dat for latitude, ttt_layer{LN}.dat for ETA, and zmax_layer{LN}.dat
for zmax where LN is Layer Number.
'''

__version__ = '0.12.2023'
__author__ = 'shyogaswara'

import numpy as np
import math
import os
import re

class Comcot2XYZ:
    '''
    Class used to generete 3 dimensional array data from comcot tsunami model
    output.
    
    ----------
    Attributes
    ----------
    layer_num : str
        a layer number string from comcot output based on their ID, ex: 03
    fpath : str
        string for file path of the layer   
          
    -------
    Methods
    -------
    get_file(layer_num)
        Generate file name string based on layer_num 
    open_file(fpath, fname)
        Open file in the path from fpath and fname
    reshape_data(line_number, data_file)
        Reshape the data from data_file so that all matrices colomn have same
        number
    generate_xyz(data_file)
        Generate XYZ from data_file that have been reshaped
    save_file(fpath, layer_num)
        Save the generated XYZ into an XYZ file in the path according to fpath
        and layer number 
    '''
    def __init__(self, layer_num, fpath):
        '''
        ----------
        Parameters
        ----------
        file : list
            file name list to be opened
        dt : list
            list of data from opened file
        x_length : int
            length from X coordinates
        line_number : int
            row number from a file to be considered as one line in list
            that needed to be equal with the length of X coordinates
        line_number_zmax : int
            row number from a file to be considered as one line in list
            that needed to be equal with the length of X coordinates for zmax
            file
        line_number_ttt : int
            row number from a file to be considered as one line in list
            that needed to be equal with the length of X coordinates for ttt
            file
        line_number2 : int
            list that consists of line_number_zmax and line_number_ttt for
            iterating purpose
        dt_reshape : list
            list of data that already reshaped
        dt_xyz : list
            list of data in XYZ format
        '''
        self.get_file(layer_num)
        self.file = [self.f_lx, self.f_ly, self.f_zmax, self.f_ttt]

        self.dt = []
        for f in self.file:
            dt = self.open_file(fpath,f)
            self.dt.append(dt.readlines())
            dt.close()
        
        self.x_length = len(self.dt[0])
        if len(self.dt[2][0].split()) == len(self.dt[3][0].split()):
            line_number = math.ceil(self.x_length/len(self.dt[2][0].split()))
        else:
            line_number_zmax = math.ceil(self.x_length/len(self.dt[2][0].split()))
            line_number_ttt = math.ceil(self.x_length/len(self.dt[3][0].split()))
            line_number2 = line_number_zmax, line_number_ttt
        
        dt_reshape=[]
        for i in self.dt[2:]:
            ln=0
            try:
                dt_reshape.append(self.reshape_data(line_number, i))
            except:
                dt_reshape.append(
                    self.reshape_data(line_number2[ln], i)
                    )
                ln += 1                
        
        self.dt_xyz=[]
        for i in dt_reshape:
            self.dt_xyz.append(self.generate_xyz(i))
    
    def get_file(self, layer_num):
        '''Get file name string from layer_num
        
        ----------
        Attributes
        ----------
        layer_num : str, int
            Layer number from comcot output ID to be processed
            can be string or integer but cannot contain alphabet characters
        
        ------
        Raises
        ------
        TypeError
            if layer_num parameters is string that contain alphabet or spaces
        
        ----------    
        Parameters
        ----------
        f_lx : str
            string of filename from layer x
        f_ly : str
            string of filename from layer y
        f_ttt : str
            string of filename from travel time layer
        f_zmax : str
            string of filename from zmax layer
        '''
        if bool(re.search('[a-zA-Z\s]+$', str(layer_num))) == True:
            raise TypeError('layer number cannot contain alphabets character')
        
        if int(layer_num) < 10:
            layer_num = f'0{int(layer_num)}'
            
        self.f_lx = f'layer{layer_num}_x.dat'
        self.f_ly = f'layer{layer_num}_y.dat'
        self.f_ttt = f'ttt_layer{layer_num}.dat'
        self.f_zmax = f'zmax_layer{layer_num}.dat'

    def open_file(self, fpath, fname):
        '''Open file name from path
        
        ----------
        Attributes
        ----------
        fpath : str
            Path of file to be opened
        
        fname : str
            filename that will be opened
        '''
        fopen = open(os.path.join(fpath, fname))
        return fopen
    
    def reshape_data(self, line_number, data_file):
        '''Reshape data from data file which is zmax and ttt layer
        where one line is a combination of line_number from file.
        ex: if line_number = 10, then the first line of reshaped data
        is combination from the 1st until the 10th line and goes on
        
        ---------
        Atributes
        ---------
        line_number : int
            row number from a file to be considered as one line in list
            that needed to be equal with the length of X coordinates
        data_file : list
            list of value from data zmax or travel time
           
        ---------- 
        Parameters
        ----------
        matrix_data : list
            list of data that have been reshaped
        dt_o : list
            data from 1st line until line_number
        res : str
            combination of data from dt_o into single str and then splitted
            by whitespaces
        data_file : list
            leftover list from data_file started from line_number onward
        '''
        matrix_data = []
        for x in range(self.x_length):
            dt_o = data_file[:line_number]
            res = " ".join(dt_o).split()
            matrix_data.append(res)
            data_file = data_file[line_number:]
        return matrix_data
    
    def generate_xyz(self,data_file):
        '''Generate 3d array data from x, y, and reshaped data of zmax and 
        travel time from reshape_data method
        
        ---------
        Atributes
        ---------
        data_file : list
            list of value from data zmax or travel time that already reshaped
        '''
        matrix_data = []
        for i, x in enumerate(self.dt[0]):
            for j, y in enumerate(reversed(self.dt[1])):
                matrix_data.append(
                    [item.strip() for item in [x,y,data_file[j][i]]]
                    )
        return matrix_data
    
    def save_file(self, fpath, layer_num):
        pass
        



if __name__=="__main__":
    MAIN_PATH = r"D:\Tsunami_Model_SUMBAR"
    FILE_PATH = r"SumBar\resSB_2layer"
    FILE_PATH = os.path.join(MAIN_PATH,FILE_PATH)

    LAYER_NUM = '2'

    dt = Comcot2XYZ(LAYER_NUM,FILE_PATH)
    