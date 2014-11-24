# -*-coding:utf-8 -
from Equipement import Equipement

class ParcMaison(Equipement) : 
    
    def __init__(self, production_par_maison = -2.5, nombre = 0): #consommation moyenne de 22000 kWh/an/maison soit -2,5kW/maison
       self.nombre=nombre      
       self.production_par_maison = production_par_maison # en kW/maison
       self.production_totale = 0.0
       self.production = 0
       
       self.PROD_MAX=production_par_maison*2.0*nombre  # consommation de 200% par maison
       self.effacement=0.0
       self.activite=50.0
       self.EFFA_MAX = 30.0 # en %
       
    
    def heure_pleine(self):
        """
        if (date["Jour"]==6 or date["Jour"]==7)and(date["Heure"]>=8 and date["Heure"]<=23) :
            return True
        else :
            if date["Heure"]>=7 and date["Heure"]<=9 :
                return True
            elif date["Heure"]>=12 and date["Heure"]<=14 :
                return True
            elif date["Heure"]>=17 and date["Heure"]<=23 :
                return True
            else :
                return False"""
        return False
    
    def ajouter(self,nombre_maisons):
        self.nombre += nombre_maisons
        print("{0} maisons dans le parc".format(self.nombre))
        for i in range(self.nombre - nombre_maisons , self.nombre):
            if self.heure_pleine() == True :
                self.production = self.production_par_maison*2  #entre 100% et 200% de conso
                self.activite = 100.0
            else :
                self.production = self.production_par_maison 
                self.activite = 50.0
            self.production_totale = self.production_totale + self.production_par_maison
        return self.production_totale 
    
    def production_elec_totale(self):
        return self.production_totale

    def donner_conso(self):
        print ("{0} maisons, production totale : {1}  kW").format(self.nombre, self.production_elec_totale())

    def effacement_maison(self, pourcentage):    
        if pourcentage < self.EFFA_MAX :
            self.production_totale=(100-pourcentage)*self.production_totale/100
            self.effacement = pourcentage
            
        else : 
            print("effacement maximum depasse")
            
        return self.production_totale
    
if __name__=="__main__":
    parc = ParcMaison()
    parc.ajouter(20)
    parc.donner_conso()
    parc.ajouter(30)
    parc.donner_conso()
    parc.effacement_maison(10)
    parc.donner_conso()
