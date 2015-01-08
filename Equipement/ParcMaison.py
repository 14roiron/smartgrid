# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global
from math import *

'''INFOS
    production = - consommation ; 
    prod_min = - conso_max = conso sans effacement ;
    prod_max = - conso_min = conso avec effacement ; => cout_max = cout pour effacer
    effacement = prod_max - prod_min --> faux ?
    attention prod_min = equipement.activite = -conso
'''

class ParcMaison (Utilitaire) : 
    def __init__(self, nom="maison", prod=-3., effa=0.1, activite=0., nombre=300): #consommation moyenne de environ 1kW/maison --> heure basse 0,7kW/maison
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre  # consommation de 2kW par maison (pic) ; attention production toujours négative
        self.EFFA_MAX=effa*self.nombre # en kWglobal
        self.activite=activite
        self.effacement=0. # en %
        self.cout=self.EFFA_MAX*(80./1000./6.)/600*10**-8#*self.nombre #a retravailler
        self.nom=nom
        self.production=[]
        for i in range(0,721):
            self.production.append(50.*(1.+cos(pi/144.*(i+30.))*cos(3.*(pi/144.*(i+30.))))) #pourcentage qui multiplié par self.PROD_MAX (<0) donne la production (<0)
        for i in range(721,1009):
            self.production.append(80*exp(-0.5*(sin(4*(pi/144*(i-12)))/sin(pi/144*(i-12)))**2)+20)
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par défaut
    
    def etatSuivant(self, consigne=0., effacement=0.):
        pourcentage = self.production[Global.temps] #% de la production à l'étape actuelle, >0
        if pourcentage >= -effacement*self.EFFA_MAX/self.PROD_MAX: #ie pourcentage * PROD_MAX <= -eff * EFFA_MAX ie la consommation est plus grande que l'effacement demandé
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX #maj de l'activité
        else:  #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self, consigne=0., effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #si la consommation est plus grande que l'effacement demandé
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else: #sinon, on considère l'effacement maximal possible
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)  
        (prod_max,cout_max)=self.prevision(0.,100.)
        return(prod_min,prod_max,cout_min,self.cout,cout_max)   
    
if __name__ == "__main__":
    maison = ParcMaison()
    print maison.cout
   
