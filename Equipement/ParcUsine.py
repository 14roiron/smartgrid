# -*-coding:Utf-8-*

from Equipement import Equipement
from Utilitaire import Global

class ParcUsine(Equipement):
    
    def __init__(self,nom="usine",prod=-3000.,effa=1000.,activite=0.,nombre=2): #consommation maximale de 3000 kW
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre #en kW global ; production négative
        self.EFFA_MAX=effa*self.nombre
        self.activite=activite
        self.effacement=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        self.nom=nom
        #construction de self.production sur une semaine (=>taille = 1008)
        jour = [0. for i in range(144)] #consommation maximale entre 7h40 et 19h00, rampes sur 7h-7h40 et 19h-19h40
        jour[43] = 25. #pourcentage qui multiplié par self.PROD_MAX (<0) donne la production (<0)
        jour[44] = 50. 
        jour[45] = 75. 
        for i in range(46,117):
            jour[i] = 100.
        jour[117] = 75. 
        jour[118] = 50.
        jour[119] = 25. 
        self.production = []
        for i in range(6):
            self.production += jour
        self.production+=[0. for i in range(144)] #usine fermée le dimanche
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par défaut
    

    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[Global.temps%144] #% de la production à l'étape actuelle, >0
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #ie pourcentage * PROD_MAX <= -eff * EFFA_MAX ie la consommation est plus grande que l'effacement demandé
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else: #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%144]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #si la consommation est plus grande que l'effacement demandé
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else: #sinon, on considère l'effacement maximal possible
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)  
        (prod_max,cout_max)=self.prevision(0.,100.) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)  
    
if __name__ == "__main__":
    usine = ParcUsine()
    print usine.production  
    print len(usine.production)
