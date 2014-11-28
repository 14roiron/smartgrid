# -*-coding:utf-8 -
from Equipement import Equipement
from  Utilitaire import Global 
from Utilitaire.Global import meteoTest


class ParcSolaire(Equipement):
    def __init__(self,nom="ParcSolaire",prod=150.,effa=0,activite=10,nb=50,meteo=meteoTest):
        '''nombre de panneaux solaires dans la ferme'''
        self.nombre = nb
        '''Trois possibilités : meteo1, meteo2 ou meteoTest'''
        self.meteo = meteo
        '''nom du Parc'''
        self.nom = nom
        self.PROD_MAX = int(prod*self.nombre)
        self.activite = activite
        self.EFFA_MAX = effa
        self.effacement = 0
        self.cout=10
        
    def prevision(self, consigne, effacement):
        """retourne l'activité à l'état suivant en pourcentage par rapport à PROD_MAX"""
        return (self.calculActivite(Global.temps+1), 0)
    
    def simulation(self):
        """pas de consigne ou d'effacement possible pour un panneau solaire :
        puissance min = puissance max et le coût est toujours le même (que le panneau produise ou pas)"""
        return (self.calculActivite(Global.temps+1), self.calculActivite(Global.temps+1), 0, 0, 0)
        
    def etatSuivant(self, consigne, effacement):
        """consignes et effacement en %"""
        self.activite = self.calculActivite(Global.temps)
        
    def contraintes(self, consigne, effacement):
        """consignes et effacement en %
        si la consigne correspond à la prochaine activité prévue pas de problème et sinon ça ne marche pas"""
        if consigne == self.calculActivite(Global.temps+1) and effacement == 0:
            return True
        else:
            return False
    
    def calculActivite(self,temps):
        """formule de test, lien avec les données météo à faire"""
        return self.meteo[temps]["GHI"])*8./100.
        
#pour les tests
if __name__=='__main__':
    a=ParcSolaire()
    a.simulation()
    a.calculActivite(Global.temps)
    Global.temps=3
    print a.meteo
    a.contraintes(60,0)
    a.etatSuivant(100, 100)
    print int(a.meteo[Global.temps]["GHI"])
    print "act:={}".format(a.activite)
    
#des tests sont à effectuer pour vérifier le comportement en profondeur mais ça semble ok!
