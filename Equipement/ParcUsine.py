from Utilitaire import Utilitaire

class ParcUsine(Equipements):
    def __init__(self,prod=0.0,effa=1000.0,activite=0,nb=2) :
        self.PROD_MAX=prod #en kW, c'est une puissance instantanée
        self.EFFA_MAX=effa
        self.nombreUsines=nb
        self.activite=activite
        self.effacement=0.0
            
    def reduireConso(self) : 
        if self.activite>=0.25*self.PROD_MAX : 
            self.activite-=0.25*self.PROD_MAX*self.nombreUsines
        else self.activite=0        
        
    def augmenterConso(self):    
        if self.activite<=0.75*self.PROD_MAX :
            self.activite+=0.25*self.PROD_MAX*self.nombreUsines
        else self.activite=self.PROD_MAX   
        
   
    def etatSuivant(self,consigne=0,effacement=0):
        if date["Jour"]==7 or date["Jour"]==6 :
            self.reduireConso()
        
        if effacement==0: 
            if 7<=date["Heure"]<=19 : 
                self.augmenterConso()
            elif date["Heure"]>19 or date["Heure"]<7 :
                self.reduireConso() 
        else :
            if 7<= date["Heure"]<=19 and self.activite>=self.PROD_MAX*(1-effacement/100)
                self.activite=self.PROD_MAX*(1-effacement/100)*self.nombreUsines
                   
        
    def tauxEffacement(self, effacement):
        if self.activite>(self.activite-self.PROD_MAX*effacement) :
            self.activite-=effacement*self.PROD_MAX*self.nombreUsines/100 #La consigne est un pourcentage de la 
                                                    #consommation maximale
     
      
    def prevision(self, consigne=0, effacement=0):
        if date["Jour"]==7 :
            return (0.0, 0.0) 
        elif date["Heure"]<=7 or date["Heure"]>20 : 
            return (0.0,0.0)
        elif effacement==0 :
            if 7<date["Heure"]<8 and date["minutes"]>=40 :
                return (100.0, 0.0)
            for i from 1 to 4 :
                if date["Heure"]==7 and date["minutes"]==i*10 :
                return (25*i, 0.0)
            elif 8<=date["Heure"]<=19 :
                return (100.0,0.0)
            for i from 1 to 4 :
                if date["Heure"]==19 and date["minutes"]==i*10 :
                return (25*i, 0.0)
            
        elif effacement!=0 :
            if 8<date[Heure]<19 :
                return(100.0,effacement*0.0000022*self.PROD_MAX*self.nombreUsines)
            if 7<=date["Heure"]<8 and date["minutes"]>=40 :
                return (100.0*(1-effacement/100), effacement*0.0000022*self.PROD_MAX*self.nombreUsines)
            for i from 1 to 4 :
                if date["Heure"]==7 and date["minutes"]==i*10 :
                return (25*i(1-effacement/100), effacement*0.0000022*25*i*self.PROD_MAX/100*self.nombreUsines)
            elif 8<=date["Heure"]<=19 :
                return (100.0*(1-effacement/100),effacement*0.0000022*self.PROD_MAX*self.nombreUsines)
            for i from 1 to 4 :
                if date["Heure"]==19 and date["minutes"]==i*10 :
                return (25*i(1-effacement/100), effacement*0.0000022*25*i*self.PROD_MAX/100*self.nombreUsines)                                                   
                                                                
                                                                
                                                                
                                                                
                                                                
                                                                #chiffre abouti
                                                               #avec 80kWh pour une usine divisé par 3600 secondes et divisé par 100
                                                               #car l'effacement est un pourcentage
            
        
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0,0)  
        (prod_max,cout_max)=self.prevision(0,100) 
        return(prod_min,prod_max,cout_min,0,cout_max)    
   
                
