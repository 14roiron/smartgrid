class ParcSolaire(Equipement):
    
    global temps
    
    def __init__(self, prod, activite, nb, lieu):
        '''caractéristique permettant de connaître le rendement du panneau solaire'''
        self.Pwc = prod
        '''nombre de panneaux solaires dans la ferme'''
        self.nb = nb
        '''Trois possibilités : Volx1 ou Volx2'''
        self.lieu = lieu
        
        self.PROD_MAX = self.nb*self.Pwc/1000*12
        self.activite = 1
        self.EFFA_MAX = 0
        self.effacement = 0
        
    def prevision(self, consigne, effacement):
        return (self.calculPuissance(temps+1), 0)
    
    def simulation(self):
        return (self.calculPuissance(temps+1), self.calculPuissance(temps+1), 0, 0, 0)
        
    def etatSuivant(self, consigne, effacement):
        puissance_apres = self.calculPuissance(temps+1)
        self.puissance = puissance_apres
        pass
        
    def contraintes(self, consigne, effacement):
        if consigne == 1 and effacement == 0:
            return True
        else:
            return False
        pass
    
    def calculPuissance(self, temps):
        return self.nb * self.Pwc / 1000 * 12
