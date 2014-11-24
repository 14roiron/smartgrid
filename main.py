
from Equipement import *
from Utilitaire import *
from Ville import Ville

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()

t=0 #t=0 -> Lun 00h00
while t<6*24*7:
    consignes=[0 for i in range(0,ville.nombreEquipementProduction-1)]
    for i in range(0,ville.nombreEquipementProduction-1):
        
    