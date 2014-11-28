# -*-coding:utf-8 -
class ParcTurbineAGaz:
    def __init__(self,nom="turbine_a_gaz",prod=1000.,effa=0.,activite=0.,nombre=12.):
        self.nom=nom
        self.nombre=nombre
        self.PROD_MAX=prod*self.nombre
        self.EFFA_MAX=effa
        self.activite=activite
        self.effacement=0.
        self.demarrage=[0.,0.,0.,0.,22.6,56.5,67.79,74.2,81.51,96.83,100.,100.,100.,98.46,96.04,94.43,94.43,94.43,94.43,94.43,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33] #courbe de montée en puissance, pas de 1 min
        self.arret=[100.,100.,100,100.,100.,100.,100.,100.,100.,30.71,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.] #courbe d'arrêt, pas de 1 min
        self.cout=self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=0.):
        if consigne>self.activite: #si on veut augmenter la puissance, on place l'activité actuelle sur la courbe de montée en puissance et on en déduit l'état à t+10min
            i=0
            while self.activite>self.demarrage[i]:
                i+=1
            if consigne<self.demarrage[i+10]: #si l'activité demandée est atteinte avant t+10min
                return (consigne,2*self.PROD_MAX*(80./1000./6.)*self.nombre) #nous avons supposé pour l'instant qu'il est deux fois plus cher de mettre la turbine en marche que de l'arrêter, ce qui explique le facteur "2". 
            else:
                return (self.demarrage[i+10],2*self.PROD_MAX*(80./1000./6.)*self.nombre) #même chose avec l'arrêt
        elif consigne<self.activite:
            i=0
            while self.activite<self.arret[i]:
                i+=1
            if consigne>self.arret[i+10]:
                return (consigne,0.5*self.cout) #voir 8 lignes plus haut pour avoir l'explication du facteur "0.5". c'est assez imprécis comme raisonnement mais pour le moment, il nous manque les données relatives au calcul de ces coûts
            else:
                return (self.arret[i+10],0.5*self.cout)
        else: #si on garde une activité constante
            return(consigne,self.cout)
            
    def simulation(self):
        (prodmin,coutmin)=self.prevision(0.,0.)
        (prodmax,coutmax)=self.prevision(100.,0.)
        return(prodmin,prodmax,coutmin,self.cout,coutmax)
        
    def etatSuivant(self,consigne=0.,effacement=0.):
        (self.activite,self.cout)=self.prevision(consigne,effacement)

if __name__=="__main__":
    a=ParcTurbineAGaz()
    a.simulation()
    print a.activite
    a.etatSuivant(100,100)
    print a.activite
    print a.prevision(100,100)
