# -*-coding:utf-8 -
from Equipement import Equipement
class Stockage(Equipement):

	def __init__(self,nom="Stockage", capacite = 50000., prop = 1./2., cout=2.,prod = 20.):
		self.capacite = capacite
		self.reste = self.capacite*prop #pas un pourcentage
		self.cout = cout
		self.PROD_MAX=prod
		self.activite = 0.

	def etatSuivant(self, consigne=0., effacement=0.):
		self.activite = consigne
		self.reste -= self.activite/100.*self.PROD_MAX*600. # on retire la puissance dégagée * 600s

	def prevision(self,consigne=0.,effacement=0.):
		puissance = self.reste - consigne/100.*self.capacite
		prix = self.cout*abs(puissance)
		return (puissance/self.capacite*100., prix)

	def simulation(self):
		if self.reste>self.PROD_MAX*600.*100.: # si on a assez d'énergie pour débiter à fond...
			prod_max=100.
		else:
			prod_max=self.reste/(self.PROD_MAX*600) 
		prix_min = 0.
		prix_stable = self.activite*self.cout*self.PROD_MAX
		prix_max = prod_max*self.PROD_MAX*self.cout
		return (0.,prod_max,prix_min,prix_stable,prix_max)

	def simulation_eff(self):
		prix_min = self.reste*self.cout
		prix_max = self.capacite*self.cout
		prix_normal = 0.
		return (0.,100., prix_min, prix_normal, prix_max)
