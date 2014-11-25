# -*-coding:utf-8 -
from Equipement import Equipement
from Utilitaire import BaseDeDonnees

class ParcSolaire(Equipement,Utilitaire):
    
    global temps
    
    def __init__(self, prod=150, activite=10, nb=50, lieu=0):
        '''nombre de panneaux solaires dans la ferme'''
        self.nb = nb
        '''Trois possibilités : Volx1 ou Volx2'''
        self.lieu = lieu
        
        self.PROD_MAX = self.nb*self.prod
        self.activite = activite
        self.EFFA_MAX = 0
        self.effacement = 0
        
    def prevision(self, consigne, effacement):
        """retourne l'actvité à l'état suivant en pourcentage par rapport à PROD_MAX"""
        return (self.calculActivite(temps+1), 0)
    
    def simulation(self):
        """pas de consigne ou d'effacement possible pour un panneau solaire :
        puissance min = puissance max et le coût est toujours le même (que le panneau produise ou pas)"""
        return (self.calculActivite(temps+1), self.calculActivite(temps+1), 0, 0, 0)
        
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
    
    def calculActivite(self, temps):
        """formule de test, lien avec les données météo à faire"""
        return 5 / 1000 * 100
    
    def eclairement(self):
    	irra=BaseDeDonnees.importerTable()
    	return(irra[temps]["GHI"],irra[temps]["DNI"],irra[temps]["DHI"])
    
    #pour les tests
if __name__=='__main__':
	a=ParcSolaire()
    
