# -*-coding:utf-8 -*
from Equipement import *
from Utilitaire.heure import Utilitaire
from Utilitaire.BaseDeDonnees import BaseDeDonnees
from Ville import Ville


"""Import de la base de données"""

db = BaseDeDonnees()
meteo1 = db.importerTable("Semaine1")
meteo2 = db.importerTable("Semaine2")
meteoTest = db.importerTable("Test")

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()
temps=0
a=Utilitaire(temps)
a.temps=temps #t=0 -> Lun 00h00
while temps<6*24*7:
    # Définition des consignes de production
    conso = sum(i.PROD_MAX*(-1)*i.activite for i in ville.equipConso) # Consommation totale pour l'étape en cours
    simulations = [i.simulation() for i in ville.equipConso]
    consignesProduction=[0 for i in range(ville.nombreEquipementProduction)]
    for i in range(ville.nombreEquipementProduction):
       #actualisation des équipements de production
       ville.equipProduction[i].etatSuivant(consignesProduction[i],0)
    consignesConso=[0 for i in range(ville.nombreEquipementConso)]
    for i in range(ville.nombreEquipementConso):
        #actualisation des équipements de Consommation
        ville.equipConso[i].etatSuivant()
    temps+=1
    
