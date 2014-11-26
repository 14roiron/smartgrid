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

exemple_conso_j = [21,22,23,23,24,24,25,25,25,24,25,26,27,28,28,29,30,30,30,29,28,27,27,28,28,29,30,30,30,32,34,36,38,40,\
42,44,46,47,48,48,48,49,50,51,52,53,54,55,55,56,56,57,56,55,54,56,57,57,56,55,54,53,50,48,47,46,45,45,45,\
45,45,45,46,47,46,45,45,47,48,49,50,50,50,51,52,51,50,51,51,50,51,53,54,57,59,60,62,62,68,69,71,73,75,77,78,\
78,77,78,79,80,82,84,82,80,79,79,80,78,75,73,70,68,65,63,60,58,57,55,55,56,54,50,48,45,43,40,38,35,33,50,28,\
26,23,20]

def ind_eqpascher(liste,consigne): #indice de l'equipement le moins cher, liste comme simulations
    i=0
    cout_min = liste[0][4]
    for j in range (1,len(liste)):
        if (liste[j][4] < cout_min and consigne[j] != liste[j][1]): #si moins cher et pas encore mis au max
            i=j
    return i

Global.db.enregistrerID(ville.equipProduction, ville.equipConso, 0)
while temps<6*24-1:#*7:
    # Définition des consignes de production
    """conso = sum(i.PROD_MAX*(-1)*i.activite for i in ville.equipConso) # Consommation totale pour l'étape en cours"""
    simulations = [i.simulation() for i in ville.equipProduction]
    prod_actuelle = sum(i.PROD_MAX*i.activite for i in ville.equipProduction)
    conso_future = exemple_conso_j[temps+1]
    diff=conso_future-prod_actuelle # différence conso-production actuelle
    consigne = [i.activite for i in ville.equipProduction] # on initialise la consigne

    if diff>0: #on consomme plus qu'on ne produit
        max=sum(simulations[i][0] for i in range(len(simulations)))

        if max>=conso_future: # si on peut atteindre la valeur de la consommation...
            prod_provisoire = prod_actuelle

            while (abs(prod_provisoire-conso_future)/conso_future > 2./100 or prod_provisoire > conso_future): #tant que ecart > 2% ou prod > conso
                ind = ind_eqpascher(simulations,consigne) #indice de l'equipement le moins cher qu'on met au max
                equip = ville.equipProduction[ind]

                while (prod_provisoire < conso_future and consigne[ind] != simulations[ind][1]):
                    consigne[ind] += (simulations[ind][1]-equip.activite)/10 #...on le met progressivement au max
                    prod_provisoire = prod_provisoire - equip.activite*equip.PROD_MAX + simulations[ind][1]*equip.PROD_MAX #maj

        else:
            for i in range (len(simulations)): # on met tout au max
                consigne[i] = simulations[i][1]
            prod_provisoire = sum(simulations[i][1]*ville.equipProduction[i].PROD_MAX for i in range(len(simulations)))

            # il faut maintenant compenser la différence prod-conso avec de l'effacement et du stockage
            
            consigne_stock=[0 for i in range(ville.nombreEquipementStockage)]
            simulations=[i.simulation() for i in ville.equipStockage]
            while ((-1)*(prod_provisoire-conso_future)/conso_future > 2./100):
                ind = ind_eqpascher(simulations,consigne_stock)
                consigne_stock[ind]=100
                prod_provisoire+=ville.equipStockage[ind].PROD_MAX
            
Global.tempsinc()#temps+=1
    

print "ok!"
