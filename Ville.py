from Equipement.ParcSolaire import ParcSolaire
from Equipement.ParcMaison import ParcMaison
from Equipement.ParcTurbineAGaz import ParcTurbineAGaz
from Equipement.ParcUsine import ParcUsine
from Equipement.ParcEolien import ParcEolien
from Equipement.Stockage import Stockage
from Utilitaire.Global import meteo1
from Utilitaire.Global import meteo2
from Utilitaire.Global import meteoTest

class Ville:

	def __init__(self):
		self.equipProduction = [ParcSolaire(nom="PVmeteo1",prod=250.,effa=10.,activite=50.,nb=10.,meteo=meteo1),\
		                        ParcSolaire("PVmeteo2",prod=250.,effa=10.,activite=50.,nb=10.,meteo=meteo1),\
		                        ParcTurbineAGaz("turbine"),\
		                        ParcEolien(nom="eolienne,meteo1",n=100.,eolienne="eolienne5",meteoVent=meteo1),\
		                        ParcEolien(nom="eolienne,meteo2",n=5.,eolienne="eolienne1500",meteoVent=meteo2)]
		self.equipConso = [ParcMaison("parc1"),\
		                   ParcUsine("Usine1")]
		self.equipStockage = [Stockage("Stockage 1")]
		self.nombreEquipementProduction = len(self.equipProduction)
		self.nombreEquipementConso = len(self.equipConso)
		self.nombreEquipementStockage = len(self.equipStockage)


#pour les tests
if __name__=='__main__':
    a=Ville()
    print a.equipConso
    print a.equipStockage
    print a.equipProduction
    

