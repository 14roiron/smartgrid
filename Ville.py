import Equipement.ParcSolaire
class Ville:

	def __init__(self):
		self.equipProduction=[]
		self.equipConso=[]
		self.nombreEquipementProduction=len(self.equipProduction)
		self.nombreEquipementConso=len(self.equipConso)
		self.equipProduction=Equipement.ParcSolaire()
		#self.equipConso+=Maisons()
