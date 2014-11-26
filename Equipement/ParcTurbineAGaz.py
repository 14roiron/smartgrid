class ParcTurbineAGaz:
    def __init__(self,prod=885,effa=0,activite=0.0,nb=3):
        self.PROD_MAX=prod
        self.EFFA_MAX=effa
        self.activite=activite
        self.effacement=0
        self.nombre=nb
        self.demarrage=[0,0,0,0,22.6,56.5,67.79,74.2,81.51,96.83,100,100,100,98.46,96.04,94.43,94.43,94.43,94.43,94.43,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33]
        self.arret=[100,100,100,100,100,100,100,100,100,30.71,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.cout=self.activite/100.0*self.PROD_MAX*(80/1000/6)*self.nombre
        
    def prevision(self,consigne):
        if consigne>self.activite:
            i=0
            while self.activite>=self.demarrage[i]:
                i+=1
            if consigne<self.demarrage[i+10]:
                return (consigne,2*self.PROD_MAX*(80/1000/6)*self.nombre)
            else:
                return (self.demarrage[i+10],2*self.PROD_MAX*(80/1000/6)*self.nombre)
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
            
    def simulation(self):
        (prodmin,coutmin)=self.prevision(0)
        (prodmax,coutmax)=self.prevision(100)
        return(prodmin,prodmax,coutmin,self.cout,coutmax)
        
    def etatSuivant(self,consigne):
        self.activite=consigne
        self.cout=self.activite/100.0*self.PROD_MAX*(80/1000/6)*self.nombre
