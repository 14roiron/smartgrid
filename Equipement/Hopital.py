## -*-coding:utf-8 -

from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global
from math import *

class Hopital(Equipement):
    def __init__(self, nom = "hopital", prod = -210., effa = 10., activite = 50.):
        Equipement.__init__(self, nom, prod, effa, activite)
        self.production = []
        for i in range(7):
            self.production = self.production + [71. for i in range(43)] + [86.] + [100. for i in range(69)] + [86.] + [71. for i in range(30)]
        self.effacement = 0.
        self.temps_effa = 0 # temps pendant lequel l'hôpital s'est effacé
        self.temps_dernier_effa = -1 # temps écoulé depuis le dernier effacement, -1 car self.etatSuivant()
        self.cout = self.effacement/100.*self.EFFA_MAX*(80./1000./6.)
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par défaut
        

    def simulation(self):
        prod_min = self.production[(Global.temps+1)%1008] # pas d'effacement 
        if (self.temps_effa >= 3 or 0 < self.temps_dernier_effa < 18):  # on ne peut pas effacer l'hôpital pendant plus de 30 minutes et il faut attendre 3h avant de l'effacer de nouveau
            prod_max = prod_min                                     #j'aime l'idée
            cout_max = 0.
            cout_stable = 0.
        else:
            prod_max = self.production[(Global.temps+1)%1008] + self.EFFA_MAX/self.PROD_MAX*100
            cout_max = self.EFFA_MAX*(80./1000./6.)
            cout_stable = self.cout
        return (prod_min, prod_max, 0., cout_stable, cout_max)

    def etatSuivant(self, consigne=0., effacement=0.):
        if effacement == 0. :
            self.effacement = 0.
            self.activite = self.production[Global.temps]
            self.temps_effa = 0
            self.temps_dernier_effa += 1
        else:
            if (self.temps_effa>=3 or 0<self.temps_dernier_effa<18):
                self.effacement = 0.
                self.activite = self.production[Global.temps]
                self.temps_effa = 0
                self.temps_dernier_effa += 1
            else:
                self.temps_effa += 1
                self.temps_dernier_effa = 0
                pourcentage=self.production[Global.temps%1008] #% de la production à  l'étape actuelle, >0
                if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #ie pourcentage * PROD_MAX <= -eff * EFFA_MAX ie la consommation est plus grande que l'effacement demandÃ©
                    self.effacement=effacement
                    self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
                else: #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
                    self.effacement=self.activite
                    self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)
            
        
       
