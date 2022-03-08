"""Runs an XFOIL analysis for a given airfoil and flow conditions"""
import shutil, os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import glob

# %% Inputs

# airfoil_name = "s4320"
datfiles = []
for file in glob.glob("../Airfoil Analyzed/*.dat"):
    file = file.replace('../Airfoil Analyzed\\','')
    datfiles.append(file.replace('.dat',''))

alpha_i = 0
alpha_f = 10
alpha_step = 0.25
Re = 205000
Mach = 0.119
n_iter = 100


# %% XFOIL input file writer 

end_recap = {}

for airfoil_name in datfiles:
    if os.path.exists("polar_file.txt"):
        os.remove("polar_file.txt")
    print(airfoil_name)
    
    input_file = open("input_file.in", 'w')
    input_file.write("LOAD ../Airfoil Analyzed\{0}.dat\n".format(airfoil_name))
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("Mach {0}\n".format(Mach))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
                                                 alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")
    input_file.close()
    
    subprocess.call("xfoil.exe < input_file.in", shell=True)
    
    polar_data = np.loadtxt("polar_file.txt", skiprows=12)
    cl = polar_data[:,1]
    cd = polar_data[:,2]
    end_factor = cl**(3/2)/cd
    polar_data = np.append(polar_data,np.transpose([end_factor]),axis=1)
    
    end_recap[airfoil_name] = np.max(end_factor)
    
    #shutil.move("../Airfoil Database\{0}.dat".format(airfoil_name), '../Airfoil Analyzed/')
    