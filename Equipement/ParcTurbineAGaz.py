class TurbineAGaz:
    
    def __init__(self,prod=885,effa=0,activite=0,nb=4):
        self.PROD_MAX=prod*nb
        self.EFFA_MAX=effa*nb
        self.activite=activite
        self.effacement=0
        self.demarrage=[100,93.55,92.7]
        self.arret=[100,30.8,0]
        self.cout=self.activite/100.0*self.PROD_MAX*(0.80/1000/6)*nb
        
    def prevision(self,consigne):
        if consigne>self.activite:
            i=0
            while self.activite>=self.demarrage[i]:
                i+=1
            if consigne<self.demarrage[i+10]:
                return (consigne,2*self.PROD_MAX*(0.80/1000/6)*nb)
            else:
                return (self.demarrage[i+10],2*self.PROD_MAX*(0.80/1000/6)*nb)
        elif consigne<self.activite:
            i=0
            while self.activite<=self.arret[i]:
                i+=1
            if consigne>self.arret[i+10]:
                return (consigne,0.5*self.cout)
            else:
                return (self.arret[i+10],0.5*self.cout)
        else:
            return(consigne,self.cout)
        
    def simulation(self,consigne):
        (prodmin,coutmin)=self.prevision(0)
        (prodmax,coutmax)=self.prevision(100)
        return(prodmin,prodmax,coutmin,self.cout,coutmax)
    
    def etatSuivant(self,consigne):
        self.activite=consigne
    
     
    
            


