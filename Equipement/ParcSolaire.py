# -*-coding:utf-8 -
from Equipement import Equipement
from  Utilitaire import Global 
from Utilitaire.Global import meteoTest


class ParcSolaire(Equipement):
    def __init__(self, nom="ParcSolaire", prod=0.260, effa=0., activite=10., nb=10., meteo=meteoTest):
        '''nombre de panneaux solaires dans la ferme'''
        self.nombre = nb
        '''Trois possibilités : meteo1, meteo2 ou meteoTest'''
        self.meteo = meteo
        self.meteoliss=[]
        for i in range (len(meteo)-1):
            self.meteoliss.append(0.5*(meteo[i]["GHI"]+meteo[i+1]["GHI"]))
        self.meteoliss.append(meteo[len(meteo)-1]["GHI"])
        '''nom du Parc'''
        self.nom = nom
        self.PROD_MAX = prod*self.nombre
        self.activite = activite
        self.EFFA_MAX = effa
        self.effacement = 0.
        self.cout = 8.31/6.*self.nombre
        
    def prevision(self, consigne=0., effacement=0.):
        """retourne l'activité à l'état suivant en pourcentage par rapport à PROD_MAX"""
        return (self.calculActivite(Global.temps+1), self.cout)
    
    def simulation(self):
        """pas de consigne ou d'effacement possible pour un panneau solaire :
        puissance min = puissance max et le coût est toujours le même (que le panneau produise ou pas)"""
        return (self.calculActivite(Global.temps+1), self.calculActivite(Global.temps+1),self.cout, self.cout, self.cout)
        
    def etatSuivant(self, consigne, effacement):
        """consignes et effacement en %"""
        self.activite = self.calculActivite(Global.temps+1)
        
    def contraintes(self, consigne, effacement):
        """consignes et effacement en %
        si la consigne correspond à la prochaine activité prévue pas de problème et sinon ça ne marche pas"""
        if consigne == self.calculActivite(Global.temps+1) and effacement == 0.:
            return True
        else:
            return False
    
    def calculActivite(self,temps):
        return (self.meteoliss[temps])/1000.*80./100.*100. #loi de murphy, on a env. 80% de la production imaginée, on divise par 1000 W . m-2, intensité de ref
        
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
