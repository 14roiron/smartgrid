# -*-coding:utf-8 -
from Equipement import Equipement
class Stockage(Equipement):

	def __init__(self, capacite = 5000., prop = 1/2, cout=2.):
		self.capacite = capacite
		self.reste = self.capacite*prop #pas un pourcentage
		self.cout = cout

	def etat_suivant(self, consigne=0., effacement=0.):   #consigne : pourcentage d'utilisation de la capacité souhaité
		self.reste = consigne*self.capacite

	def prevision(self,consigne=0.,effacement=0.):
		puissance = self.reste - consigne*self.capacite
		prix = self.cout*abs(puissance)
		return (puissance/self.capacite*100, prix)

	def simulation(self):
		prix_min = self.reste*self.cout
		prix_max = self.capacite*self.cout
		prix_normal = 0.
		return (0.,100., prix_min, prix_normal, prix_max)

	def simulation_eff(self):
		prix_min = self.reste*self.cout
		prix_max = self.capacite*self.cout
		prix_normal = 0.
		return (0.,100., prix_min, prix_normal, prix_max)
