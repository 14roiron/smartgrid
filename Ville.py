import Equipement.ParcSolaire
import Equipement.ParcMaison

class Ville:

	def __init__(self):
		self.equipProduction=[]
		self.equipConso=[]
		self.equipProduction=Equipement.ParcSolaire()
		self.equipConso+=Equipement.ParcMaison()
		self.nombreEquipementProduction=len(self.equipProduction)
		self.nombreEquipementConso=len(self.equipConso)