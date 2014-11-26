# -*-coding:utf-8 -
from Equipement import Equipement
from  Utilitaire import Global 
from Utilitaire.Global import meteoTest


class ParcSolaire(Equipement):
    
    def __init__(self, prod=150, activite=10, nb=50, meteo=meteoTest, nom="ParcSolaire"):
        '''nombre de panneaux solaires dans la ferme'''
        self.nb = nb
        '''Trois possibilités : meteo1, meteo2 ou meteoTest'''
        self.meteo = meteo
        '''nom du Parc'''
        self.nom = nom
        
        self.PROD_MAX = self.nb*prod
        self.activite = activite
        self.EFFA_MAX = 0
        self.effacement = 0
        
    def prevision(self, consigne, effacement):
        """retourne l'activité à l'état suivant en pourcentage par rapport à PROD_MAX"""
        return (self.calculActivite(Global.temps+1), 0)
    
    def simulation(self):
        """pas de consigne ou d'effacement possible pour un panneau solaire :
        puissance min = puissance max et le coût est toujours le même (que le panneau produise ou pas)"""
        temps= Global.temps
        return (self.calculActivite(temps+1), self.calculActivite(temps+1), 0, 0, 0)
        
    def etatSuivant(self, consigne, effacement):
        """consignes et effacement en %"""
        temps=Global.temps
        self.activite = self.calculActivite(temps+1)
        
    def contraintes(self, consigne, effacement):
        """consignes et effacement en %
        si la consigne correspond à la prochaine activité prévue pas de problème et sinon ça ne marche pas"""
        temps=Global.temps
        if consigne == self.calculActivite(temps+1) and effacement == 0:
            return True
        else:
            return False
    
    def calculActivite(self):
        """formule de test, lien avec les données météo à faire"""
        temp=Global.temps
        return self.meteo[temps]["GHI"] / 1000 * 100
        
#pour les tests
if __name__=='__main__':
    a=ParcSolaire()
    a.simulation()
    a.calculActivite()
    
#des tests sont à effectuer pour vérifier le comportement en profondeur mais ça semble ok!
