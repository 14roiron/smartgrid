# -*-coding:Utf-8-*

from Equipement import Equipement
from Utilitaire import Global

class ParcUsine(Equipement):
    
    def __init__(self,nom="usine",prod=-1500.,effa=1000.,activite=0.,nombre=5,production=[]): #consommation maximale de 3000 kW
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre #en kW global ; production nÃ©gative
        self.EFFA_MAX=effa*self.nombre*(10**-8)
        self.activite=activite
        self.effacement=0.
        self.cout=self.EFFA_MAX*(80./1000./6.)*self.nombre*10
        self.nom=nom
        #construction de self.production sur une semaine (=>taille = 1008)
        jour = [0. for i in range(144)] #consommation maximale entre 7h40 et 19h00, rampes sur 7h-7h40 et 19h-19h40
        for i in range(10):
            jour[35+i]=10.*i #augmentation progressive
            jour[125-i]=10.*i #baisse progressive
        for i in range(45,116):
            jour[i] = 100.
        self.production = []
        for i in range(6):
            self.production += jour
        self.production+=[0. for i in range(144)] #usine fermée le dimanche
        #for i in range(109,133):
            #self.production[i]=0
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par défaut
    

    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[Global.temps%1008] #% de la production à l'étape actuelle, >0
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #ie pourcentage * PROD_MAX <= -eff * EFFA_MAX ie la consommation est plus grande que l'effacement demandé
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else: #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
            self.effacement=self.activite
            self.activite=0.
        self.cout=self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #si la consommation est plus grande que l'effacement demandé
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else: #sinon, on considère l'effacement maximal possible
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)  
        (prod_max,cout_max)=self.prevision(0.,100.) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)  
    
    
    
class ParcUsine38(Equipement):
    
    def __init__(self,nom="usine38",prod=-1000.,effa=1000.,activite=0.,nombre=7, production=[]): #consommation maximale de 3000 kW
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre #en kW global ; production négative
        self.EFFA_MAX=effa*self.nombre
        self.activite=activite
        self.effacement=0.#why ??
        self.cout=self.EFFA_MAX*(2.*80./1000./6.)*self.nombre #effacement 2X plus cher que pour une usine normale
        self.nom=nom
        self.production = []
        #construction de self.production sur une semaine (=>taille = 1008)
        jour = [95. for i in range(144)] #consommation sur la journée
        for i in range(3):
            jour[i] = 80. + 5.*i
            jour[48 + i] = 80. + 5.*i
            jour[96 + i] = 80. + 5.*i
            jour[48 - i] = 80. + 5.*i
            jour[96 - i] = 80. + 5.*i
            jour[143 - i] = 85. + 5.*i
        for i in range(7):
            self.production += jour
        self.etatSuivant() #initialisation de la variable activite selon le moment de la journée ; effacement nul par dÃ©faut
    

    def etatSuivant(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008] #% de la production à l'étape actuelle, >0
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #ie pourcentage * PROD_MAX <= -eff * EFFA_MAX ie la consommation est plus grande que l'effacement demandÃ©
            self.effacement=effacement
            self.activite=pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX
        else: #sinon on coupe totalement la consommation en faisant l'effacement maximal possible
            self.effacement=self.activite
            self.activite=0.
        self.cout=2*self.effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        pourcentage=self.production[(Global.temps+1)%1008]
        if pourcentage>=-effacement*self.EFFA_MAX/self.PROD_MAX: #si la consommation est plus grande que l'effacement demandÃ©
            return (pourcentage+effacement*self.EFFA_MAX/self.PROD_MAX,effacement/100.*self.EFFA_MAX*(80./1000./6.)*self.nombre)
        else: #sinon, on considère l'effacement maximal possible
            return (0.,-pourcentage/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0.,0.)  
        (prod_max,cout_max)=self.prevision(0.,100.) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)
    
if __name__ == "__main__":
    usine = ParcUsine38()
    print usine.production  
    print len(usine.production)
