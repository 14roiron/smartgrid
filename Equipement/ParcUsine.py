# -*-coding:Utf-8-*

from Equipement import Equipement

class ParcUsine(Equipement):
    
    global temps
    
    def __init__(self,prod=3000.0,effa=1000.0,activite=0,nb=2) :
        self.PROD_MAX=prod*nb #en kW, c'est une puissance instantanée
        self.EFFA_MAX=effa*nb
        self.nb=nb
        self.activite=activite
        self.effacement=effa
        self.cout=self.effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nb
        self.prod=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 25.0, 50.0, 75.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 75.0, 50.0, 25.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
    
    def etatSuivant(self,consigne=0,effacement=0):
        p=self.prod[temps%7]
        if p>=effacement*self.EFFA_MAX/self.PROD_MAX:
            activite=p-effacement*self.EFFA_MAX/self.PROD_MAX
        else:
            activite=0.0
        
    def prevision(self,consigne=0,effacement=0):
        p=self.prod[(temps+1)%7]
        if p>=effacement*self.EFFA_MAX/self.PROD_MAX:
            return (p-effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nb)
        else :
            return (0,p/100.0*self.PROD_MAX*(0.80/1000/6)*self.nb)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0,0)  
        (prod_max,cout_max)=self.prevision(0,100) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)    
   
                
