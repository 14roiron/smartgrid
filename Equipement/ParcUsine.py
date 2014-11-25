import class Utilitaire
class ParcUsine(Equipements):
    def __init__(self, nombreUsines=5) :
        self.nombreUsines=nombreUsines 
        self.activite=0.0
        self.prod_max=3000.00 #en kW, c'est une puissance instantanée
        self.effacement=0.0
        self.EFFA_MAX=1000.00
        
            
    def reduireConso(self) : 
        if self.activite>=0.25*self.prod_max : 
            self.activite-=0.25*self.prod_max*self.nombreUsines
        else self.activite=0        
        
    def augmenterConso(self):    
        if self.activite<=0.75*self.prod_max : 
            self.activiten+=0.25*self.prod_ma*self.nombreUsines
        else self.activite=self.prod_max   
        
   
    def etatSuivant(self,consigne=0,effacement=0):
        if date["Jour"]==7 or date["Jour"]==6 :
            self.reduireConso
        
        if effacement==0: 
            if 7<=date["Heure"]<=19 : 
                self.augmenterConso()
            elif date["Heure"]>19 or date["Heure"]<7 :
                self.reduireConso() 
        else :
            if 7<= date["Heure"]<=19 and self.activite>=self.prod_max*(1-effacement/100)
                self.activite=self.prod_max*(1-effacement/100)*self.nombreUsines
                   
        
    def tauxEffacement(self, effacement):
        if self.activite>(self.activite-self.prod_max*effacement) :
            self.activite-=effacement*self.prod_max*self.nombreUsines/100 #La consigne est un pourcentage de la 
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
                return(100.0,effacement*0.0000022*self.prod_max*self.nombreUsines)
            if 7<=date["Heure"]<8 and date["minutes"]>=40 :
                return (100.0*(1-effacement/100), effacement*0.0000022*self.prod_max*self.nombreUsines)
            for i from 1 to 4 :
                if date["Heure"]==7 and date["minutes"]==i*10 :
                return (25*i(1-effacement/100), effacement*0.0000022*25*i*self.prod_max/100*self.nombreUsines)
            elif 8<=date["Heure"]<=19 :
                return (100.0*(1-effacement/100),effacement*0.0000022*self.prod_max*self.nombreUsines)
            for i from 1 to 4 :
                if date["Heure"]==19 and date["minutes"]==i*10 :
                return (25*i(1-effacement/100), effacement*0.0000022*25*i*self.prod_max/100*self.nombreUsines)                                                   
                                                                
                                                                
                                                                
                                                                
                                                                
                                                                #chiffre abouti
                                                               #avec 80kWh pour une usine divisé par 3600 secondes et divisé par 100
                                                               #car l'effacement est un pourcentage
            
        
    def simulation(self):
        (prod_min,cout_min)=self.prevision(0,0)  
        (prod_max,cout_max)=self.prevision(0,100) 
        return(prod_min,prod_max,cout_min,0,cout_max)    
   
                
