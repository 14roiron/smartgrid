# -*-coding:utf-8 -
class ParcTurbineAGaz:
    def __init__(self,nom="turbine_a_gaz",prod=885.,effa=0.,activite=0.,nb=3):
        self.nom=nom
        self.PROD_MAX=prod
        self.EFFA_MAX=effa
        self.activite=activite
        self.effacement=0.
        self.nombre=nb
        """courbe de montée en puissance"""
        self.demarrage=[0.,0.,0.,0.,22.6,56.5,67.79,74.2,81.51,96.83,100.,100.,100.,98.46,96.04,94.43,94.43,94.43,94.43,94.43,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33]
        """courbe d'arrêt"""
        self.arret=[100.,100.,100,100.,100.,100.,100.,100.,100.,30.71,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
        self.cout=self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        """si on veut augmenter la puissance, on place l'activité actuelle sur la courbe de montée en puissance
        et on en déduit l'état à t+1"""
        if consigne>self.activite:
            i=0
            while self.activite>=self.demarrage[i]:
                i+=1
            """si l'activité demandée peut-être atteinte avant t+1"""
            if consigne<self.demarrage[i+10]:
                return (consigne,2*self.PROD_MAX*(80./1000./6.)*self.nombre)
            else:
                return (self.demarrage[i+10],2*self.PROD_MAX*(80./1000./6.)*self.nombre)
            """même chose avec l'arrêt"""
        elif consigne<self.activite:
            i=0
            while self.activite<=self.arret[i]:
                i+=1
            if consigne>self.arret[i+10]:
                return (consigne,0.5*self.cout)
            else:
                return (self.arret[i+10],0.5*self.cout)
            """si on garde une activité constante"""
        else:
            return(consigne,self.cout)
            
    def simulation(self):
        (prodmin,coutmin)=self.prevision(0.,0.)
        (prodmax,coutmax)=self.prevision(100.,0.)
        return(prodmin,prodmax,coutmin,self.cout,coutmax)
        
    def etatSuivant(self,consigne=0.,effacement=0.):
        self.activite=consigne
        self.cout=self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre
if __name__=="__main__":
    a=ParcTurbineAGaz()
    #a.etatSuivant(100, 100)
    a.simulation()
    print a.activite
    a.etatSuivant(100, 100)
    print a.activite
    print a.prevision(100, 100)
    #bordel le code est faux il devrait mettre au moins une demi-heure pour faire 0-100%