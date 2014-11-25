# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global

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
        
        date=Utilitaire.calculDate(Global.temps)
        if (date["Jour"]==6 or date["Jour"]==7)and(date["Heure"]>=8 and date["Heure"]<22) :
            return True
        else :
            if date["Heure"]>=7 and date["Heure"]<9 :
                return True
            elif date["Heure"]>=12 and date["Heure"]<14 :
                return True
            elif date["Heure"]>=17 and date["Heure"]<22 :
                return True
            else :
                return False

    def heure_moyenne_montante(self):
        date=Utilitaire.calculDate(Global.temps)
        if (date["Jour"]==6 or date["Jour"]==7)and(date["Heure"]>=7 and date["Heure"]<8):
            return True
        else :
            if date["Heure"]>=6 and date["Heure"]<7 :
                return True
            elif date["Heure"]>=11 and date["Heure"]<12 :
                return True
            elif date["Heure"]>=16 and date["Heure"]<17 :
                return True
            else :
                return False
                
    def heure_moyenne_descendante(self):
        date=Utilitaire.calculDate(Global.temps)
        if (date["Jour"]==6 or date["Jour"]==7)and(date["Heure"]>=22 and date["Heure"]<23):
            return True
        else :
            if date["Heure"]>=9 and date["Heure"]<10 :
                return True
            elif date["Heure"]>=14 and date["Heure"]<15 :
                return True
            elif date["Heure"]>=22 and date["Heure"]<23 :
                return True
            else :
                return False
    
    def ajouter(self,nombre_maisons):
        date=Utilitaire.calculDate(Global.temps)
        self.nombre += nombre_maisons
        print("{0} maisons dans le parc".format(self.nombre))
        for i in range(self.nombre - nombre_maisons , self.nombre):
            if self.heure_pleine() == True :
                self.production = self.production_par_maison*2  #entre 100% et 200% de conso
                self.activite = 100.0
            elif self.heure_moyenne_montante() == True:
                self.production = self.production_par_maison*(date["Minutes"]/60.0+1) # rampe entre 100% et 200%
            elif self.heure_moyenne_descendante()== True :
                self.production = self.production_par_maison*((60-date["Minutes"])/60.0+1)
            else :
                self.production = self.production_par_maison 
                self.activite = 50.0
            self.production_totale = self.production_totale + self.production_par_maison
        return self.production_totale 
    
    def production_elec_totale(self):
        date=Utilitaire.calculDate(Global.temps)
        for i in range(self.nombre, self.nombre):
            if self.heure_pleine() == True :
                self.production = self.production_par_maison*2  #entre 100% et 200% de conso
                self.activite = 100.0
            elif self.heure_moyenne_montante() == True:
                self.production = self.production_par_maison*(date["Minutes"]/60.0+1) # rampe entre 100% et 200%
            elif self.heure_moyenne_descendante()== True :
                self.production = self.production_par_maison*((60-date["Minutes"])/60.0+1)
            else :
                self.production = self.production_par_maison 
                self.activite = 50.0
            self.production_totale = self.production_totale + self.production_par_maison
        return self.production_totale

    def donner_conso(self):
        print ("{0} maisons, production totale : {1}  kW").format(self.nombre, self.production_elec_totale())

    def effacement_maison(self, pourcentage):    
        if pourcentage < self.EFFA_MAX :
            self.production_totale=(100-pourcentage)*self.production_totale/100
            self.effacement = pourcentage
            
        else : 
            print("effacement maximum depasse")
            
        return self.effacement
    
    def simulation(self):
        prod_max = 2*self.production_par_maison*self.nombre
        prod_min = self.production_par_maison*self.nombre
        cout_min = -80/6000.0*self.production_par_maison 
        cout_max = -80/3000.0*self.production_par_maison
        #print(prod_max, prod_min, cout_min, cout_max)
        return (prod_max, prod_min, cout_min, cout_max)
    
    def etat_suivant(self, consigne=0, effacement=0):
       date=Utilitaire.calculDate(Global.temps)
       self.production_totale = self.production_elec_totale()
       self.effacement = self.effacement_maison()
       self.activite = self.production_totale/self.PROD_MAX
       
    
    def prevision(self):
        date=Utilitaire.calculDate(Global.temps)
        temps_minutes = 60*date["Heure"]+date["Minutes"]
        if date["Jour"]==6 or date["Jour"]==7 :
            if temps_minutes>470 and temps_minutes<1310 :    #de 7h50 à 22h50
                return self.production_par_maison*2*self.nombre
            elif temps_minutes>350 and temps_minutes<470 :
                return self.production_par_maison*((temps_minutes-350)/60.0+1)*self.nombre
            elif temps_minutes>1310 and temps_minutes<1370:
                return self.production_par_maison*((1370-temps_minutes)/60+1)*self.nombre
            else :
                return self.production_par_maison*self.nombre
        else :
            if (temps_minutes>410 and temps_minutes<530) or (temps_minutes>710 and temps_minutes<830) or (temps_minutes>1010 and temps_minutes<1310):
                return self.production_par_maison*2*self.nombre
            elif (temps_minutes>360 and temps_minutes<410) or (temps_minutes>660 and temps_minutes<710) or (temps_minutes>960 and temps_minutes<1010):
                return self.production_par_maison * ((date["Minutes"]+10)/60+1)*self.nombre
            elif (temps_minutes>540 and temps_minutes<590) or (temps_minutes>840 and temps_minutes<890) or (temps_minutes>1320 and temps_minutes<1380):
                return self.production_par_maison * ((50-date["Minutes"])/60+1)*self.nombre
            else :
                return self.production_par_maison*self.nombre
