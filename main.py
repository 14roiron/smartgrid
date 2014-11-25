# -*-coding:utf-8 -*
from Equipement import *
from Utilitaire import *
from Utilitaire.BaseDeDonnees import BaseDeDonnees
from Ville import Ville

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()

t=0 #t=0 -> Lun 00h00
while t<6*24*7:
    # Définition des consignes de production
    conso = sum(i.PROD_MAX*(-1)*i.activite for i in ville.equipConso) # Consommation totale pour l'étape en cours
    simulations = [i.simulation() for i in ville.equipConso]
    consignesProduction=[0 for i in range(ville.nombreEquipementProduction)]
    for i in range(ville.nombreEquipementProduction):
       #actualisation des équipements de production
       ville.equipProduction[i].etatSuivant(consignesProduction[i])
    consignesConso=[0 for i in range(ville.nombreEquipementConso)]
    for i in range(ville.nombreEquipementConso):
        #actualisation des équipements de Consommation
        ville.equipConso[i].etatSuivant()
    t+=1
    
