from Equipement.ParcSolaire import ParcSolaire
#from Equipement.ParcMaison import ParcMaison
from Equipement.ParcTurbineAGaz import ParcTurbineAGaz
from Utilitaire.Global import meteo1
from Utilitaire.Global import meteo2
from Utilitaire.Global import meteoTest

exemple_conso_j = [21,22,23,23,24,24,25,25,25,24,25,26,27,28,28,29,30,30,30,29,28,27,27,28,28,29,30,30,30,32,34,36,38,40,\
                   42,44,46,47,48,48,48,49,50,51,52,53,54,55,55,56,56,57,56,55,54,56,57,57,56,55,54,53,50,48,47,46,45,45,45,\
                   45,45,45,46,47,46,45,45,47,48,49,50,50,50,51,52,51,50,51,51,50,51,53,54,57,59,60,62,62,68,69,71,73,75,77,78,\
                   78,77,78,79,80,82,84,82,80,79,79,80,78,75,73,70,68,65,63,60,58,57,55,55,56,54,50,48,45,43,40,38,35,33,50,28,\
                   26,23,20]

class Ville:

	def __init__(self):
		self.equipProduction=[ParcSolaire(250,10,50,meteo1),ParcSolaire(250,10,50,meteo2),
							  ParcTurbineAGaz()]
		self.equipConso=[]#ParcMaison()]
		self.equipStockage=[]
		self.nombreEquipementProduction=len(self.equipProduction)
		self.nombreEquipementConso=len(self.equipConso)
		self.nombreEquipementStockage=len(equipStockage)

#pour les tests
if __name__=='__main__':
	#ParcSolaire(10,20,20,30)
	a=Ville()
	print a.equipConso
	
