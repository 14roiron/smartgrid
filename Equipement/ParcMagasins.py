# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global

class ParcMagasins (Utilitaire) : # des commerces de centre ville aux petits supermarchés
    def __init__(self,nom="magasins",prod=-140,effa=50,activite=0,nombre=20):
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre
        self.EFFA_MAX=effa*self.nombre
        self.activite=activite
        self.effacement=0. # en %
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        self.production=[0. for i in range(0,1009)]
        for i in range (0,1009):  #eteint entre 8h et 18h  864
            if i>864 :   #magasins fermés le dimanche et entre 19h et 9h
                self.production[i]=10. # en %
            elif (i%144>54 and i%144<112) :
                self.production[i]=100.
            elif (i%144>=46 and i%144<54):
                self.production[i] = self.production[i-1]+10
            elif (i%144>=112 and i%144<120):  
                self.production[i] = self.production[i-1]-10
            else :
                self.production[i]=10. #consommation des vitrines/frigo/etc...
    
    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[Global.temps]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else:
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #production supérieure à l'effacement
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else :
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.) 
        (prod_max,cout_max)=self.prevision(0.,100.)
        return(prod_min,prod_max,cout_min,self.cout,cout_max)      
