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
    def __init__(self, nom="maison", prod=-2., effa=0.1, activite=0., nb=300.): #consommation moyenne de environ 1kW/maison -->heure basse 0,7kW/maison
        self.nombre=nb
        self.PROD_MAX=prod*self.nombre  # consommation de 2kW par maison (pic) Attention production toujours négative
        self.EFFA_MAX=effa*self.nombre # en kWglobal
        self.activite=activite
        self.effacement=0. # en %
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        self.production=[]
        for i in range(0,721):
            self.production.append(50.*(1.+cos(pi/144.*(i+30.))*cos(3.*(pi/144.*(i+30.))))) #pourcentage qui multiplié par self.PROD_MAX (<0) donne la production (<0)
        for i in range(721,1008):
            self.production.append(50.*(1.+cos(pi/72.*(i-792.))))
    
    def etatSuivant(self, consigne=0., effacement=0.):
        p = self.production[Global.temps] #% de la production à l'étape actuelle, >0
        if p >= -effacement*self.EFFA_MAX/self.PROD_MAX: #ie p * PROD_MAX <= -eff * EFFA_MAX ie consommation plus grande l'effacement demandé
            self.effacement=effacement
            self.activite=p+effacement*self.EFFA_MAX/self.PROD_MAX #maj de l'activité
        else:
            self.effacement=self.activite #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self, consigne=0., effacement=0.):
        p=self.production[(Global.temps+1)%1008] #si l'effacement demandé est inférieur à la consommation...
        if p>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            return (p+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else :
            return (0.,-p/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(-2.0,0.)  
        (prod_max,cout_max)=self.prevision(0.43*self.nombre-self.EFFA_MAX,100.)  #minimum de la conso*nombre de maisons - effacement max 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)      
