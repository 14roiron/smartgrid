# -*-coding:utf-8 -
from Equipement import Equipement
class Stockage(Equipement):

	def __init__(self,nom="Stockage", capacite = 10000., prop = 1./2., cout=2., prod = 20.):
		self.capacite = capacite
		self.reste = self.capacite*prop #pas un pourcentage
		self.cout = cout
		self.PROD_MAX=prod
		self.activite = 0.
		self.EFFA_MAX = 0.
		self.effacement = 0.
		self.nom = nom

	def etatSuivant(self, consigne=0., effacement=0.):
		self.activite = consigne
		self.reste = max(0., self.reste - self.activite/100.*self.PROD_MAX*600.) # on retire la puissance dégagée * 600s

	def simulation(self):
		if self.reste > self.PROD_MAX*600.: # si on a assez d'énergie pour débiter à fond...
			prod_max=100.
		else:
			prod_max= self.reste*100./(self.PROD_MAX*600.) 
                        if prod_max < 10**(-3):
                            prod_max =0.
		prix_min = 0.
		prix_stable = self.activite/100.*self.cout*self.PROD_MAX
		prix_max = prod_max/100.*self.PROD_MAX*self.cout
		return (0.,prod_max,prix_min,prix_stable,prix_max)
	
if __name__ == "__main__":
    stockage = Stockage()
    print stockage.capacite
    print stockage.reste
    s = stockage.simulation()
    print s
    stockage.etatSuivant(s[1], 0.)
    print stockage.reste
    s = stockage.simulation()
    print s
    stockage.etatSuivant(s[1], 0.)
    print stockage.reste
    s = stockage.simulation()
    print s
    stockage.etatSuivant(s[1], 0.)
    print stockage.reste
    s = stockage.simulation()
    print s
    stockage.etatSuivant(s[1], 0.)
    print stockage.reste
    s = stockage.simulation()
    print s
    stockage.etatSuivant(s[1], 0.)
    
