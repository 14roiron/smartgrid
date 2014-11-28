# -*-coding:Utf-8 -*
from Equipement import Equipement
from Utilitaire.heure import Utilitaire
from Utilitaire import Global

class ParcMagasins (Utilitaire) : # des commerces de centre ville aux petits supermarchés
    def __init__(self,nom="magasins",prod=-140.,effa=50.,activite=0.,nombre=20):
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre
        self.EFFA_MAX=effa*self.nombre
        self.activite=activite
        self.effacement=0. # en %
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        jour=[10. for i in range(0,144)] #magasins fermés entre 19h et 9h, mais consommation des vitrines/frigo/etc...
        for i in range(46,54):
            jour[i]=jour[i-1]+10.
        for i in range(54,112):
            jour[i]=100.
        for i in range(112,120):
            jour[i]=jour[i-1]-10.
        self.production=[]
        for i in range(6):
            self.production += jour
        self.production += [10. for i in range(0,144)] #magasins fermés le dimanche
        self.production
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par défaut 
    
    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[Global.temps]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX:
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else:
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #production supérieure à l'effacement
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else :
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.) 
        (prod_max,cout_max)=self.prevision(0.,100.)
        return(prod_min,prod_max,cout_min,self.cout,cout_max)      
