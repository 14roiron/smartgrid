# -*-coding:utf-8 -*
from Equipement import *
from Utilitaire import *
from Utilitaire.BaseDeDonnees import BaseDeDonnees
from Ville import Ville

"""Import de la base de données"""

db = BaseDeDonnee()
meteo1 = db.importerTable("Semaine1")
meteo2 = db.importerTable("Semaine2")
meteoTest = db.importerTable("Test")

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()

t=0 #t=0 -> Lun 00h00
<<<<<<< HEAD
while t<1:#6*24*7:

    consignesProduction=[0 for i in range(0,ville.nombreEquipementProduction-1)]
    for i in range(0,ville.nombreEquipementProduction-1):
=======
while t<6*24*7:
    # Définition des consignes de production
    conso = sum(i.PROD_MAX*(-1)*i.activite for i in ville.equipConso) # Consommation totale pour l'étape en cours
    simulations = [i.simulation() for i in ville.equipConso]
    consignesProduction=[0 for i in range(ville.nombreEquipementProduction)]
    for i in range(ville.nombreEquipementProduction):
>>>>>>> cf7d09e9b3a4fc5467be79956d49bb39ec83d6ad
       #actualisation des équipements de production
       ville.equipProduction[i].etatSuivant(consignesProduction[i])
    consignesConso=[0 for i in range(ville.nombreEquipementConso)]
    for i in range(ville.nombreEquipementConso):
        #actualisation des équipements de Consommation
        ville.equipConso[i].etatSuivant()
    t+=1
    
