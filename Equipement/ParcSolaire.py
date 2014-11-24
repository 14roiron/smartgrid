# -*-coding:utf-8 -
from Equipement import Equipement

class ParcSolaire(Equipement):
    
    global temps
    
    def __init__(self, prod=150, activite=10, nb=50, lieu=0):
        '''caractéristique permettant de connaître le rendement du panneau solaire'''
        self.Pwc = prod
        '''nombre de panneaux solaires dans la ferme'''
        self.nb = nb
        '''Trois possibilités : Volx1 ou Volx2'''
        self.lieu = lieu
        
        self.PROD_MAX = self.nb*self.Pwc/1000*12
        self.activite = 1
        self.EFFA_MAX = 0
        self.effacement = 0
        
    def prevision(self, consigne, effacement):
        """prototype des fonctions, retour?"""
        return (self.calculPuissance(temps+1), 0)
    
    def simulation(self):
        """prototype des fonctions, retour?"""
        return (self.calculPuissance(temps+1), self.calculPuissance(temps+1), 0, 0, 0)
        
    def etatSuivant(self, consigne, effacement):
        """consignes et effacement en %"""
        puissance_apres = self.calculPuissance(temps+1)
        self.puissance = puissance_apres
        
    def contraintes(self, consigne, effacement):
        """consignes et effacement en %"""
        if consigne == 100 and effacement == 0:
            return True
        else:
            return False
    
    def calculPuissance(self, temps):
        """formule de test?"""
        return self.nb * self.Pwc / 1000 * 12
    
    
    #pour les tests
if __name__=='__main__':
	a=ParcSolaire()
    
