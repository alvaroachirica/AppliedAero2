#CST_airfoil_fit
import imp
import math
import pandas
import matplotlib.pyplot as plt  
df = pandas.read_excel('OurAirfoil.xlsx')
#w = [0.2540,0.3427,0.2938,0.3533,0.2134,0.5397,-0.0990,-0.0392,0.0363,0.1981,0.0978,0.5023]
#get the values for a given column
XL = df[2].values
XU = df[3].values
XU = XU[:-9]

def CST2coords(W,dz):
    xl = list(XL)
    for x in xl:
        if x < 0:
            xl.pop(xl.index(x))
    for x in xl:
        if x < 0:
            xl.pop(xl.index(x))
    xu = list(XU)
    for x in xu:
        if x < 0:
            xu.pop(xu.index(x))
    wl = W[:int(0.5*len(W))]
    wu = W[int(0.5*len(W)):]
    x = xl + xu
    N1 = 0.5
    N2 = 1
    yl =[]
    yu = []
    yl = ClassShapeF(wl,xl,N1,N2,-dz)
    yu = ClassShapeF(wu,xu,N1,N2,dz)
    y_coords = yl+yu
    return x,y_coords

def ClassShapeF(w,x,N1,N2,dz):
    y = []
    #Class C function OK
    C = []
    for i in x:
        C.append((i**N1)*(1-i)**N2)
    #Shape S function OK
    K = []
    n = len(w)-1
    
    for i in range(0,n+1):
        K.append((math.factorial(n))/((math.factorial(i))*(math.factorial(n-i))))
    
    S = []
    for i in range(0,len(x)):
        S_calc = 0
        for j in range(0,n+1):
            S_calc = S_calc + w[j]*K[j]*x[i]**(j)*((1-x[i])**(n-(j))) #EL FALLO EST ICI
        S.append(S_calc)

    for i in range(0,len(x)):
        y.append(C[i]*S[i]+x[i]*dz)

    return y


