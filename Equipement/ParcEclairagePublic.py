# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global

class ParcEclairagePublic (Utilitaire) : 
    def __init__(self,nom="eclairage_public",prod=-0.112,effa=0.112,activite=0,nombre=600): #consommation moyenne de environ 0,112 kW/hab avec 2hab/maison
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre  # consommation de 0.112 kW/hab pour l'éclairage en régime permanent
        self.EFFA_MAX=effa*self.nombre # en kW global -- effacement total possible
        self.activite=activite
        self.effacement=0. # en %
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        self.production=[0. for i in range(0,1009)]
        for i in range (0,1009):  #eteint entre 8h et 18h
            if i%144>48 and i%144<108 :
                self.production[i]=0.
            else :
                self.production[i]=100.
    
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
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else :
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)
        (prod_max,cout_max)=self.prevision(0.,100.)
        return(prod_min,prod_max,cout_min,self.cout,cout_max)      
