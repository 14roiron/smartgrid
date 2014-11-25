from Utilitaire import Utilitaire

class ParcUsine(Equipements):
    
    global temps
    
    def __init__(self,prod=3000.0,effa=1000.0,activite=0,nb=2) :
        self.PROD_MAX=prod*nb #en kW, c'est une puissance instantanée
        self.EFFA_MAX=effa*nb
        self.nombreUsines=nb
        self.activite=activite
        self.effacement=0.0
        self.cout=self.effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines
            
    def reduireConso(self) : 
        if self.activite>=25.0 : 
            self.activite-=25.0
        else self.activite=0.0        
        
    def augmenterConso(self):    
        if self.activite<=75.0 :
            self.activite+=25.0
        else self.activite=100.0
        
    def etatSuivant(self,consigne=0,effacement=0):
        date=Utilitaire.date
        if date["Jour"]>=6 :
            self.reduireConso()
        if 7<=date["Heure"]<=19 : 
            self.augmenterConso()
        elif date["Heure"]>19 or date["Heure"]<7 :
            self.reduireConso()
        if self.activite>=effacement*EFFA_MAX/PROD_MAX:
            self.activite-=effacement*EFFA_MAX/PROD_MAX
      
    def prevision(self, consigne=0, effacement=0):
        jour = 1 + (temps+1)/6/24 
        heure = ((temps+1)/6) % 24
        minute = (temps+1)*10 % 60 
        date = {"Mois":mois,"Jour":jour,"Heure":heure,"Minute":minute}
        if date["Jour"]>=6 or date["Heure"]<=6 or date["Heure"]>=20 or (date["Heure"]==19 and date["Minute"]>=40): 
            return (0.0,0.0)
        elif 8<=date["Heure"]<=18 or (date["Heure"]==7 and date["Minute"]>=40):
            return (100.0-effacement*EFFA_MAX/PROD_MAX),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)
        elif date["Heure"]==7 :
            for i from 0 to 3 :
                if date["Minute"]==i*10 :
                return (25*i*(1-effacement*EFFA_MAX/PROD_MAX/100),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)
        elif date["Heure"]==19 :
            for i from 0 to 3 :
                if date["Minute"]==i*10 :
                return (25*(4-i)*(1-effacement*EFFA_MAX/PROD_MAX/100),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)                                                   
                                                                
                                                                
                                                                
                                                                
                                                                
                                                                #chiffre abouti
                                                               #avec 80kWh pour une usine divisé par 3600 secondes et divisé par 100
                                                               #car l'effacement est un pourcentage
            
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0,0)  
        (prod_max,cout_max)=self.prevision(0,100) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)    
   
                
