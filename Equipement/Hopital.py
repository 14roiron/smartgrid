# -*- coding : UTF-8 -*-

from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global
from math import *

class Hopital(Equipement):
    def __init__(self, nom = "hopital", prod = -300, effa = 10., activite = 50.):
        Equipement.__init__(self, nom, prod, effa, activite)
        self.production = []
        for i in range(7):
            self.production = self.production + [50. for i in range(43)] + [60.] + [70. for i in range(69)] + [60.] + [50. for i in range(30)]
        self.effacement = 0.
        self.temps_effa = 0 # temps pendant lequel l'hôpital s'est effacé
        self.temps_dernier_effa = 0 # temps écoulé depuis le dernier effacement
        self.cout = 10. # coût arbitraire, de l'ordre de celui de 100 maisons : on efface l'hôpital le moins souvent possible
        

    def simulation(self):
        prod_min = self.production[Global.temps + 1] # pas d'effacement 
        if (self.temps_effa >= 3 or self.temps_dernier_effa <18):  # on ne peut pas effacer l'hôpital pendant plus de 30 minutes et il faut attendre 3h avant de l'effacer de nouveau
            prod_max = prod_min                                    #j'aime l'idée
            cout_max = 0
        else:
            prod_max = self.production[Global.temps + 1] - self.EFFA_MAX/self.PROD_MAX*100
            cout_max = self.cout*self.EFFA_MAX
        cout_stable = self.cout*self.effacement*self.PROD_MAX/100.
        return (prod_min, prod_max, 0., cout_stable, cout_max)

    def etatSuivant(self, consigne, effacement):
        if effacement == 0. :
            self.effacement = 0.
            self.activite = self.production[Global.temps + 1]
            self.temps_effa = 0
            self.temps_dernier_effa += 1
        else:
            self.effacement = effacement
            self.activite = self.production[Global.temps + 1] + effacement*self.EFFA_MAX/self.PROD_MAX
            self.temps_effa += 1
            self.temps_dernier_effa = 0
