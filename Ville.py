from Equipement.ParcSolaire import ParcSolaire
from Equipement.ParcMaison import ParcMaison

class Ville:

	def __init__(self):
		self.equipProduction=ParcSolaire()
		self.equipConso=ParcMaison()
		self.nombreEquipementProduction=len((self.equipProduction,))
		self.nombreEquipementConso=len((self.equipConso,))

#pour les tests
if __name__=='__main__':
	#ParcSolaire(10,20,20,30)
	a=Ville()
	print a.equipConso
	