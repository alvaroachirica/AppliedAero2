# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 18:04:35 2022

@author: alvaroms
"""
import numpy as np
import glob
import os

datfiles = []
k = 0
for file in glob.glob("*.dat"):
    print(file)
    
    i = 0
    string_list = []
    
    my_file = open(file)
    string_list = my_file.readlines()
    
    my_file.close()
    
    if string_list[1] == ' \n':
        string_list[1] = '\n'
    
    if string_list[1] != '\n':
        if float(string_list[1][-4:-2]) > 1 or float(string_list[1][-5:-2]) > 1:
            string_list = np.delete(string_list,1,0)
            
    for i in range(2,len(string_list)-2):
        for j in range(0,10):
            if string_list[i][j] != ' ':
                if (float(string_list[i][j:j+4]) == 1) or (float(string_list[i][j:j+6]) == 0.9999):
                    string_list[2:i+1] = string_list[i:1:-1]
                    string_list = np.delete(string_list,i+1,0)
                    break
                break
    
    my_file = open(file, "w")
    new_file_contents = "".join(string_list)
    
    my_file.write(new_file_contents)
    my_file.close()
    k += 1