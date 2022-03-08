import numpy as np
import matplotlib.pyplot as plt
#import the xfoil module
from xfoil import XFoil
from xfoil import model

def xfoil_calc(x,y,AoA_min,AoA_max,AoA_step):
    #create an object that has the functions of xfoil
    xf = XFoil()
    #build the airfoil objetct
    x_arr = np.array(x)
    y_arr = np.array(y)
    test_airfoil = model.Airfoil(x_arr,y_arr)
    #the airfoil of the xf object is:
    xf.airfoil = test_airfoil
    #set the reynolds
    xf.Re = 250000
    xf.M  = 0.119
    xf.n_crit = 9
    xf.xtr = (1.0,1.0) #top and bottom trip location
    #set the max iterations
    xf.max_iter = 200
    #extract to a tupple the information
    aero_data=xf.aseq(AoA_min,AoA_max,AoA_step)
    return aero_data

def aero_processing(xfoil_res):
    "Creates a dict k: AoA v: list of aero properties"
    alphas,cls,cds,cms,cps = xfoil_res
    dic = {}
    i=0
    for AoA in alphas:
        dic[AoA] = []
        dic[AoA].append(cls[i])
        dic[AoA].append(cds[i])
        dic[AoA].append(cms[i])
        dic[AoA].append(cps[i])
        i += 1
    return dic

def extract_coords(txt_file):
    "Transform txt coordinates file into 2 x,y arrays ready for XFOIL"
    infile = open(txt_file)
    source = infile.readlines()
    infile.close()
    x_coord = []
    y_coord = []
    for line in source[1:]:
        splitted = line.split(' ')
        x_coord.append(splitted[0])
        if splitted[1] == '':
            y_coord.append(splitted[2])
        else:
            y_coord.append(splitted[1])
    x_arr = np.array(x_coord)
    y_arr = np.array(y_coord)
    return x_arr,y_arr

def extract_coords2(txt_file):
    "Transform txt coordinates file into 2 x,y arrays ready for XFOIL"
    infile = open(txt_file)
    source = infile.readlines()
    infile.close()
    x_coord = []
    y_coord = []
    for line in source[1:]:
        splitted = line.split('\t')
        x_coord.append(splitted[0])
        if splitted[1] == '':
            y_coord.append(splitted[2])
        else:
            y_coord.append(splitted[1])
    x_arr = np.array(x_coord)
    y_arr = np.array(y_coord)
    return x_arr,y_arr

def plotCL(dic):
    xplot = np.fromiter(dic.keys(), dtype=float)
    yplot = np.empty_like(xplot)
    for v in dic.values():
        np.append(yplot,v[1])
    plt.legend(['Lift'])
    plt.xlabel('Angle of attack')
    plt.ylabel('CL') 
    plt.plot(xplot,yplot)
    plt.show()

def optcl(x,y,target):
    #create an object that has the functions of xfoil
    xf = XFoil()
    #build the airfoil objetct
    x_arr = np.array(x)
    y_arr = np.array(y)
    test_airfoil = model.Airfoil(x_arr,y_arr)
    #the airfoil of the xf object is:
    xf.airfoil = test_airfoil
    #set the reynolds
    xf.Re = 250000
    xf.M  = 0.119
    xf.n_crit = 9
    xf.xtr = (1.0,1.0) #top and bottom trip location
    #set the max iterations
    xf.max_iter = 200
    #extract to a tupple the information
    aero_data=xf.cl(target)
    return aero_data

def aero_processingCL(xfoil_res,target):
    "Creates a dict k: AoA v: list of aero properties"
    alpha,cd,cm,cp = xfoil_res
    endurance = (target**(3/2))/(cd)
    return endurance