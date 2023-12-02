'''
This code is used to convert comcot output from each layer into XYZ file either 
for zmax (inundation), or ETA. the output will be layer{LN}_x.dat for longitude,
 layer{LN}_y.dat for latitude, ttt_layer{LN}.dat for ETA, and zmax_layer{LN}.dat
for zmax.
'''

__version__ = '0.12.2023'
__author__ = 'shyogaswara'

import numpy as np
import math
import os

class Comcot2xyz:
    def __init__(self, layer_num, fpath):
        self.get_file(layer_num)
        self.file = [self.f_lx, self.f_ly, self.f_zmax, self.f_ttt]

        self.dt = []
        for f in self.file:
            dt = self.open_file(fpath,f)
            self.dt.append(dt.readlines())
            dt.close()
        
        x_length = len(self.dt[0])
        if len(self.dt[2][0].split()) == len(self.dt[3][0].split()):
            line_number = math.ceil(x_length/len(self.dt[2][0].split()))
        else:
            line_number_zmax = math.ceil(x_length/len(self.dt[2][0].split()))
            line_number_ttt = math.ceil(x_length/len(self.dt[3][0].split()))
            line_number2 = line_number_zmax, line_number_ttt
        
        dt_reshape=[]
        for i in self.dt[2:]:
            ln=0
            try:
                dt_reshape.append(self.reshape_data(x_length, line_number, i))
            except:
                dt_reshape.append(self.reshape_data(x_length, line_number2[ln], i))
                ln += 1                
        
        self.dt_xyz=[]
        for i in dt_reshape:
            self.dt_xyz.append(self.generate_xyz(i))
    
    def get_file(self, layer_num):
        self.f_lx = f'layer{layer_num}_x.dat'
        self.f_ly = f'layer{layer_num}_y.dat'
        self.f_ttt = f'ttt_layer{layer_num}.dat'
        self.f_zmax = f'zmax_layer{layer_num}.dat'

    def open_file(self, fpath, fname):
        fopen = open(os.path.join(fpath, fname))
        return fopen
    
    def reshape_data(self, x_length, line_number, data_file):
        matrix_data = []
        for x in range(x_length):
            dt_o = data_file[:line_number]
            res = " ".join(dt_o).split()
            matrix_data.append(res)
            data_file = data_file[line_number:]
        return matrix_data
    
    def generate_xyz(self,data_file):
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

    LAYER_NUM = "02"

    dt = Comcot2xyz(LAYER_NUM,FILE_PATH)
    