from Utilitaire import Utilitaire

class ParcUsine(Equipements):
    def __init__(self,prod=3000.0,effa=1000.0,activite=0,nb=2) :
        self.PROD_MAX=prod*nb #en kW, c'est une puissance instantanée
        self.EFFA_MAX=effa*nb
        self.nombreUsines=nb
        self.activite=activite
        self.effacement=0.0
        self.cout=self.effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines
            
    def reduireConso(self) : 
        if self.activite>=25 : 
            self.activite-=25
        else self.activite=0.0        
        
    def augmenterConso(self):    
        if self.activite<=75 :
            self.activite+=25
        else self.activite=100.0
        
   
    def etatSuivant(self,consigne=0,effacement=0):
        date=Utilitaire.date
        if date["Jour"]==7 or date["Jour"]==6 :
            self.reduireConso()
        
        if effacement==0: 
            if 7<=date["Heure"]<=19 : 
                self.augmenterConso()
            elif date["Heure"]>19 or date["Heure"]<7 :
                self.reduireConso() 
        else :
            if 7<= date["Heure"]<=19 and self.activite>=100-effacement
                self.activite=100-effacement
                   
      
    def prevision(self, consigne=0, effacement=0):
        date=Utilitaire.date
        if date["Jour"]==7 :
            return (0.0, 0.0) 
        elif date["Heure"]<=7 or date["Heure"]>20 : 
            return (0.0,0.0)
        if date["Heure"]==7 and date["Minute"]>=40 :
                return (100-effacement*EFFA_MAX/PROD_MAX,effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)
        for i from 1 to 4 :
                if date["Heure"]==7 and date["Minute"]==i*10 :
                return (25*i*(1-effacement*EFFA_MAX/PROD_MAX/100),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)
        elif 8<=date["Heure"]<=19 :
                return (100.0*(1-effacement*EFFA_MAX/PROD_MAX/100),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)
        for i from 1 to 4 :
                if date["Heure"]==19 and date["Minute"]==i*10 :
                return (25*(4-i)*(1-effacement*EFFA_MAX/PROD_MAX/100),effacement/100.0*self.EFFA_MAX*(0.80/1000/6)*self.nombreUsines)                                                   
                                                                
                                                                
                                                                
                                                                
                                                                
                                                                #chiffre abouti
                                                               #avec 80kWh pour une usine divisé par 3600 secondes et divisé par 100
                                                               #car l'effacement est un pourcentage
            
        
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0,0)  
        (prod_max,cout_max)=self.prevision(0,100) 
        return(prod_min,prod_max,cout_min,self.cout,cout_max)    
   
                
