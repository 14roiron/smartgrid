# -*-coding:utf-8 -*
from Equipement import *
from Utilitaire import *
from Ville import Ville

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()

t=0 #t=0 -> Lun 00h00
while t<1:#6*24*7:
    consignesProduction=[0 for i in range(0,ville.nombreEquipementProduction-1)]
    for i in range(0,ville.nombreEquipementProduction-1):
       #actualisation des équipements de production
       ville.equipProduction.etatSuivant(i)
    consignesConso=[0 for i in range(0,ville.nombreEquipementConso)]
    for i in range(0,ville.nombreEquipementConso-1):
        #actualisation des équipements de Consommation
        ville.equipConso.etatSuivant(i)
    print consignesConso
    t+=1
    
