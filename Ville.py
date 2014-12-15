from Equipement.ParcSolaire import ParcSolaire
from Equipement.ParcMaison import ParcMaison
from Equipement.ParcTurbineAGaz import ParcTurbineAGaz
from Equipement.ParcUsine import ParcUsine, ParcUsine38
from Equipement.ParcEolien import ParcEolien
from Equipement.Stockage import Stockage
from Equipement.ParcEclairagePublic import ParcEclairagePublic
from Equipement.Hopital import Hopital
from Equipement.ParcBatterieLithiumIon import ParcBatterieLithiumIon
from Equipement.ParcMagasins import ParcMagasins
from Utilitaire.Global import meteo1
from Utilitaire.Global import meteo2
from Utilitaire.Global import meteo3
from Utilitaire.Global import meteo4
from Utilitaire.Global import meteo5
from Utilitaire.Global import meteoTest

class Ville:

	def __init__(self):
		self.equipProduction = [ParcTurbineAGaz("turbine1",varcout=1.,nombre=1),\
 		                        ParcTurbineAGaz("turbine2",varcout=1.10,nombre=0.5),\
 		                        #ParcTurbineAGaz("turbine3",varcout=1.13,nombre=1),\
   		                     	ParcSolaire(nom="PVmeteo1",prod=4.,activite=50.,nb=100.,meteo=meteo1),\
  		                        ParcSolaire(nom="PVmeteo2",prod=4.,activite=50.,nb=100.,meteo=meteo2),\
  		                        ParcSolaire(nom="PVmeteo3",prod=4.,activite=50.,nb=100.,meteo=meteo3),\
  		                        ParcSolaire(nom="PVmeteo4",prod=4.,activite=50.,nb=100.,meteo=meteo4),\
  		                        ParcSolaire(nom="PVmeteo5",prod=4.,activite=50.,nb=100.,meteo=meteo5),\
  		                        ParcEolien(nom="eolienne,meteo1",n=100., eolienne="eolienne5", meteoVent=meteo1),\
  		                        ParcEolien(nom="eolienne,meteo2",n=1., eolienne="eolienne1500", meteoVent=meteo2),\
  		                        ParcEolien(nom="eolienne,meteo3",n=100., eolienne="eolienne5", meteoVent=meteo3),\
  		                        ParcEolien(nom="eolienne,meteo4",n=1., eolienne="eolienne1500", meteoVent=meteo4),\
  		                        ParcEolien(nom="eolienne,meteo5",n=10., eolienne="eolienne275", meteoVent=meteo5),\
		                        ]
		self.equipConso = [#ParcUsine38(nom="usine2-38",prod=-60.,effa=10.,activite=0.,nombre=1),\
						   ParcMaison("Maison1", prod=-2., effa=0.1, activite=0., nombre=600),\
		                   ParcUsine("Usine1",prod=-50.,effa=10.,activite=0.,nombre=5,),\
		                   ParcEclairagePublic(prod=-0.140,effa=0.112,activite=0,nombre=2400),\
                           ParcMagasins(prod=-10.,effa=2.,activite=0.,nombre=20),
                           Hopital(nom = "hopital", prod = -240., effa = 10., activite = 50.)]
		self.equipStockage = [Stockage(),Stockage(),Stockage()]#,ParcBatterieLithiumIon()]
		self.nombreEquipementProduction = len(self.equipProduction)
		self.nombreEquipementConso = len(self.equipConso)
		self.nombreEquipementStockage = len(self.equipStockage)


#pour les tests
if __name__=='__main__':
    a=Ville()
    print a.equipConso
    print a.equipStockage
    print a.equipProduction
    

