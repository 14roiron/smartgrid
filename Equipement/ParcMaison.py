# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global
from math import *

class ParcMaison (Utilitaire) : 
    def __init__(self, production = 1, nombre = 0): #consommation moyenne de environ 1kW/maison -->heure basse 0,7kW/maison
       self.nombre=nombre      
       self.production = production # en kW/maison
       self.production_totale = 0.0
       self.production = 0
       
       self.PROD_MAX=2.0*nombre  # consommation de 2kW par maison (pic)
       self.effacement=0.0 # en %
       self.activite=50.0
       self.EFFA_MAX = 0.1 # en kWglobal 
    
    def ajouterMaison(self,nombre_maisons):
        self.nombre += nombre_maisons
        print("{0} maisons dans le parc".format(self.nombre))
        
    def consommation_maison(self):
        temps=Global.temps
        if temps>720 and temps<=1008:
            self.production = -1-cos(pi/72*(temps-792))
        else :
            self.production = -1 - cos(pi/144.0*(temps+30.0))*cos(3.0*(pi/144.0*(temps+30)))
        return self.production
    
    def production_elec_totale(self):
        self.production_totale = self.production * self.nombre
        return self.production_totale
        

    def donner_conso(self):
        temps=Global.temps
        print ("{0} minutes , total production : {1}  kW").format(temps*10, self.production_elec_totale())

    def effacement_maison(self, pourcentage=0):  
        self.effacement_absolu =  pourcentage*self.consommation_maison()/100.0
        if self.effacement_absolu< self.EFFA_MAX :
            self.production_totale=(100-pourcentage)*self.production_totale/100
            self.effacement = pourcentage
        else : 
            print("effacement maximum depasse")    
        return self.production_totale
    
    def simulation(self):
        prod_max = 2*self.nombre                 # en kW
        prod_min = 0.437*self.nombre
        cout_min = -80/6000.0*self.production_par_maison #en € par maison
        cout_max = -80/3000.0*self.production_par_maison  #en € par maison
        return prod_max, prod_min, cout_min, cout_max
    
    def etat_suivant(self, consigne=0, effacement=0):
        temps=Global.temps
        self.production = self.consommation_maison()
        self.production_totale = self.production_elec_totale()
        self.production_totale = self.effacement_maison()
        if self.PROD_MAX!=0 :
            self.activite = self.production_totale/self.PROD_MAX*100.0  #en %
        else :
            self.activite = 0
       
    
    def prevision(self):
        if temps>=720 and temps < 1008 :
            self.consommation_prevue = -1-cos(pi/72*(temps-791))
        else :
            self.consommation_prevue =  -1-cos(pi/144.0*(temps+31.0))*cos(3.0*(pi/144.0*(temps+31.0)))
        #print (self.consommation_prevue)
        return self.consommation_prevue   
            
if __name__=='__main__':
    temps =0
    parc = ParcMaison()
    parc.ajouterMaison(100)
    while temps<=1008 :
        parc.donner_conso()
        parc.prevision()
        parc.etat_suivant()
        temps+=1
