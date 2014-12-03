# -*-coding:utf-8 -
class ParcTurbineAGaz:
    def __init__(self,nom="turbine_a_gaz",prod=885.,effa=0.,activite=20.,varcout = 1., nombre=3., ):
        self.nom=nom
        self.nombre=nombre
        self.varcout=varcout
        self.PROD_MAX=prod*self.nombre
        self.EFFA_MAX=effa
        self.activite=activite
        self.effacement=0.
        #self.demarrage=[0.,22.6,32.,56.5,67.79,74.2,81.51,96.83,100.,100.,100.,98.46,96.04,94.43,94.43,94.43,94.43,94.43,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33,92.33] #courbe de montée en puissance, pas de 1 min
        self.demarrage=[0.,22.6,38.,51.,51.]
        #self.arret=[100.,100.,100.,100.,100.,100.,100.,100.,100.,30.71,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.] #courbe d'arrêt
        self.arret=[50.,35.,10.,0.,0.]
        self.cout=self.varcout*self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre
        
    def prevision(self,consigne=0.,effacement=-1.):
        if consigne==0. and effacement==-1.:
            return (self.activite,(self.varcout*self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre))
        print "prix turbine: %f"%(1000. + 2.*self.varcout*consigne/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
        if consigne > self.activite+1. : #si on veut augmenter la puissance, on place l'activité actuelle sur la courbe de montée en puissance et on en déduit l'état à t+10min, 1. pour les flottants
            if self.activite < 50.: #on suppose que la courbe de charge ne fonctionne qu'au démarrage (ie avant 50%)
                i=0
                while self.activite > self.demarrage[i]:
                    i+=1
                if consigne <= self.demarrage[i+1]: #si l'activité demandée est atteinte avant t+10min
                    
                    return (consigne,1000. + 2.*self.varcout*consigne/100.*self.PROD_MAX*(80./1000./6.)*self.nombre) #nous avons supposé pour l'instant qu'il est deux fois plus cher de mettre la turbine en marche que de garder un fonctionnement constant, ce qui explique le facteur "2". 
                else:
                    return (self.demarrage[i+1],1000. + 2.*self.varcout*self.demarrage[i+1]/100.*self.PROD_MAX*(80./1000./6.)*self.nombre) 
            else:
                return (consigne, self.varcout*consigne/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
        elif consigne < self.activite-1.: #même chose avec l'arrêt
            if self.activite < 50.:
                i=0
                while self.activite <= self.arret[i]:
                    i+=1
                if consigne > self.arret[i+1]:
                    return (consigne,1000. + 0.5*self.varcout*self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre) #voir 8 lignes plus haut pour avoir l'explication du facteur "0.5". c'est assez imprécis comme raisonnement mais pour le moment, il nous manque les données relatives au calcul de ces coûts
                else:
                    return (self.arret[i+1],1000. + 0.5*self.varcout*self.activite/1000.*self.PROD_MAX*(80./10000./6.)*self.nombre)
            else:
                return (consigne, self.varcout*consigne/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
        else: #si on garde une activité constante
            return (consigne,self.varcout*consigne/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
        #return (consigne,self.varcout*self.activite/100.*self.PROD_MAX*(80./1000./6.)*self.nombre)
    def simulation(self):
        (prodmin,coutmin)=self.prevision(0.,0.)
        (prodmax,coutmax)=self.prevision(100.,0.)
        return(prodmin,prodmax,coutmin,self.cout,coutmax)
        
    def etatSuivant(self,consigne=0.,effacement=0.):
        (self.activite,self.cout)=self.prevision(consigne,effacement)

if __name__=="__main__":
    l=[]
    a=ParcTurbineAGaz()
    for i in range(100):
        a.etatSuivant(32.,0)
        l.append(a.activite)
    print l
