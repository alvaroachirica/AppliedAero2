import numpy as np
import matplotlib.pyplot as plt
import random
#import the xfoil module
from XFOILadapted import *
from CST import *
from datetime import datetime


class Airfoil2D_Optimization():
    def __init__(self,mutation_rate,n_ind,n_gen,n_selec,params_dim,w,mutate_margin,AoA,target):
        self.mutation_rate = mutation_rate
        self.n_ind         = n_ind
        self.n_gen         = n_gen
        self.n_selec       = n_selec
        self.params_dim    = params_dim
        self.w             = w
        self.mutate_margin = mutate_margin
        self.AoA           = AoA
        self.target        = target

    def create_ind(self):
        "Creates the DNA of the airfoil to optimize"
        Wopt_0 = self.w
        "Creates a candidate, represented as a string of the parameters of the airfoil"
        individual = []
        for param in Wopt_0:
            individual.append(random.uniform(param*0.9, param*1.1))
        return individual
    
    def create_pop(self):
        "Calls the create_ind func n_ind times to create the population"
        return [self.create_ind() for _ in range(self.n_ind)]
    
    def fitness(self,ind):  #he quitado AoA de input
        "Get coords.txt of the airfoil"
        xy_coods = CST2coords(ind,0)
        x_s,y_s = xy_coods
        x_arr = np.array(x_s)
        y_arr = np.array(y_s)
        plt.plot(x_arr,y_arr)
        "Calls the xfoil to calculate how good is the individual"
        ind_xfoil_calc = xfoil_calc(x_s,y_s,0.0,15,0.5)
        "Extract from xfoil dic the endurance"
        ind_dic = aero_processing(ind_xfoil_calc)
        if self.AoA < 2.0: #MAKES AOA OF 1,1.5 AND 2 WORST DESIGNS
            try:
                aero_coefs1 = ind_dic[self.AoA - 1.0] #aqui
                e1 = ((aero_coefs1[0])**(3/2))/(aero_coefs1[1])
                aero_coefs2 = ind_dic[self.AoA] #aqui
                e2 = ((aero_coefs2[0])**(3/2))/(aero_coefs2[1])
                aero_coefs3 = ind_dic[8.0] #PONGO 8 PARA MANTENER LA CURVA A RALLA
                e3 = ((aero_coefs3[self.AoA + 2.0])**(3/2))/(aero_coefs3[1])
                endurance = e1*0.3+e2*0.4+e3*0.3
                print(e2)
                return  endurance
            except KeyError:
                return 0
        else:
            try:
                aero_coefs1 = ind_dic[self.AoA - 2.0] #aqui
                e1 = ((aero_coefs1[0])**(3/2))/(aero_coefs1[1])
                aero_coefs2 = ind_dic[self.AoA] #aqui
                e2 = ((aero_coefs2[0])**(3/2))/(aero_coefs2[1])
                aero_coefs3 = ind_dic[self.AoA + 2.0] #aqui
                e3 = ((aero_coefs3[0])**(3/2))/(aero_coefs3[1])
                endurance = e1*0.3+e2*0.4+e3*0.3
                print(e2)
                return  endurance
            except KeyError:
                return 0

    def fitness2(self,ind):  #he quitado AoA de input
        "Get coords.txt of the airfoil"
        xy_coods = CST2coords(ind,0)
        x_s,y_s = xy_coods
        x_arr = np.array(x_s)
        y_arr = np.array(y_s)
        plt.plot(x_arr,y_arr)
        "Calls the xfoil to calculate how good is the individual"
        ind_xfoil_calc = optcl(x_s,y_s,self.target)
        ind_xfoil_calc2 = optcl(x_s,y_s,1.7)
        "Extract from xfoil dic the endurance"
        endurance1 = aero_processingCL(ind_xfoil_calc,self.target)
        endurance2 = aero_processingCL(ind_xfoil_calc2,1.7)
        endurance = endurance1*0.7 + endurance2*0.3
        print(endurance1)
        if endurance > 0:
            return endurance
        else:
            return 0
            

    def selection(self,pop):
        best_ind = [(self.fitness(i), i) for i in pop]
        best_ind = [i[1] for i in sorted(best_ind)] # PROBLEMA
        plt.axis('equal')
        plt.show()
        return best_ind[len(best_ind)-self.n_selec:]

    def selection2(self,pop):
        best_ind = [(self.fitness2(i), i) for i in pop]
        best_ind = [i[1] for i in sorted(best_ind)] # PROBLEMA
        plt.axis('equal')
        plt.show()
        return best_ind[len(best_ind)-self.n_selec:]

    def crossover(self,bests):
        "Select 2 parents to have a child, this func must be implemented n_ind/gen - selected times"
        crossover_point = random.randint(1,self.params_dim)
        parent1_index = random.randint(0,len(bests))
        parent2_index = random.randint(0,len(bests))
        p1_part = bests[parent1_index-1][:crossover_point]
        p2_part = bests[parent2_index-1][crossover_point:]
        child = p1_part + p2_part
        return child

    def mutation(self,ind):
        "Mutates the gnome, I need to change the mutation"
        for alelo in ind:
            pos = 0
            for alelo2 in ind[pos:]:
                pos += 1
                distance = (alelo-alelo2)/alelo
                if distance < 0.1:
                    if random.uniform(0,1) < self.mutation_rate:
                        first_g = alelo
                        second_g = alelo2
                        ind[ind.index(alelo)] = second_g
                        ind[ind.index(alelo2)]= first_g
        return  ind
    
    def mutation2(self,ind):
        for alelo in range(0,len(ind)):
            coin = 0
            if  random.uniform(0,1) < 0.5:
                coin = 1 - self.mutate_margin
            else:
                coin = 1 + self.mutate_margin
            if random.uniform(0,1) < self.mutation_rate:
                ind[alelo] = ind[alelo]*coin
        return ind

#FIRST ITERATION
Wopt8 = [0.2519,0.4024,0.1901,0.4725,-0.1081,0.0368,0.1146,0.3948]
Wopt12 = [0.2604,0.3322,0.3017,0.3578,0.1960,0.5599,-0.0955,-0.0385,0.0267,0.2170,0.0766,0.5175]


startTime = datetime.now()
print('Optimization started for CL = 1.33')
print('First population:')
Wopt8 = [0.2519,0.4024,0.1901,0.4725,-0.1081,0.0368,0.1146,0.3948]
Wopt12 = [0.2604,0.3322,0.3017,0.3578,0.1960,0.5599,-0.0955,-0.0385,0.0267,0.2170,0.0766,0.5175]
gen = Airfoil2D_Optimization(0.07,26,12,8,12,Wopt12,0.19,4.0,1.33)
init_pop = gen.create_pop()
bests = gen.selection2(init_pop)
childs = []
for i in range(0,int(gen.n_ind-gen.n_selec)):
    childs.append(gen.crossover(bests))
    new_pool = bests + childs
    next_gen = []
for new in new_pool:
    next_gen.append(gen.mutation2(new))

for generation in range(1,gen.n_gen):
    print("Generation: {}".format(generation))
    bests = []
    childs = []
    new_pool = []
    bests = gen.selection2(next_gen)
    next_gen = []
    for i in range(0,int(gen.n_ind-gen.n_selec)):
        childs.append(gen.crossover(bests))
    new_pool = bests + childs
    for new in new_pool:
        next_gen.append(gen.mutation2(new))

print(datetime.now() - startTime)




def PostProcess(results,index):
    candidate = results[index]
    xc,yc = CST2coords(candidate,0)
    xo,yo = CST2coords(Wopt12,0)
    plt.plot(xc,yc)
    plt.plot(xo,yo)
    plt.legend(['Candidate','Original'])
    plt.xlabel('x/c')
    plt.ylabel('')  
    plt.show()
    c = [xc, yc] 
    with open("candidateCL_6.txt", "w") as file:
        for x in zip(*c):
            file.write("{0}\t{1}\n".format(*x))
    

