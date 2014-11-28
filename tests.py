# -*-coding:utf-8 -*


#from Equipement import *

from Ville import Ville
from Utilitaire.heure import Utilitaire
from Utilitaire import Global
from Utilitaire.Global import temps
from Utilitaire.Global import meteo1
from Utilitaire.Global import meteo2
from Utilitaire.Global import meteoTest
from Utilitaire.BaseDeDonnees import BaseDeDonnees

"""Import de la base de données"""

"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()

temps=0 #t=0 -> Lun 00h00
Global.db.vide_table()
Global.db.enregistrerID(ville.equipProduction, ville.equipConso, ville.equipStockage, 0)
#print len(Global.meteo1)
print len(Global.meteo2)
while Global.temps < 6*24*7: #boucle principale

    consigne=[100. for i in range(len(ville.equipProduction))]
    consigne_stock=[100. for i in (range(len(ville.equipStockage)))]
    consigne_conso=[100. for i in (range(len(ville.equipConso)))]
    
    for i in range(len(consigne)):
        
        ville.equipProduction[i].etatSuivant(consigne[i],0.)
    
    for i in range(len(consigne_stock)):
        
        ville.equipStockage[i].etatSuivant(consigne_stock[i],0.)
    
    for i in range(len(consigne_conso)):
        
        ville.equipConso[i].etatSuivant(0.,consigne_conso[i])
    

    Global.db.enregistrerEtape(ville.equipProduction, ville.equipConso, ville.equipStockage, 0)        
    Global.tempsinc()#temps+=1
    print Global.temps
    

print "ok!"
