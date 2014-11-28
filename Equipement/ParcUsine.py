# -*-coding:Utf-8-*

from Equipement import Equipement
from Utilitaire import Global

class ParcUsine(Equipement):
    
    def __init__(self,nom="usine",prod=-3000.,effa=1000.,activite=0.,nombre=2) :
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre #en kW, c'est une puissance instantanée
        self.EFFA_MAX=effa*self.nombre
        self.activite=activite
        self.effacement=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        self.production = [0. for i in range(144)]
        self.production[43] = 25.
        self.production[44] = 50. 
        self.production[45] = 75. 
        for i in range(46,117):
            self.production[i] = 100.
        self.production[117] = 75. 
        self.production[118] = 50.
        self.production[119] = 25. 
    
    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[Global.temps%144]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else:
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%144]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else :
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)  
        (prod_max,cout_max)=self.prevision(0.,100.) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)  
    
if __name__ == "__main__":
    usine = ParcUsine()
    print usine.production  
    print len(usine.production)
