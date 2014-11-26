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

def ind_eqpascher(liste,consigne): #indice de l'equipement le moins cher, liste comme simulations
    i=0
    cout_min = liste[0][4]
    for j in range (1,len(liste)):
        if (liste[j][4] < cout_min and consigne[j] != liste[j][1]): #si moins cher et pas encore mis au max
            i=j
    return i


Global.db.enregistrerID(ville.equipProduction, ville.equipConso, 0)
#print len(Global.meteo1)
#print len(Global.meteo2)
while Global.temps<6*24*7: #boucle principale
    """conso = sum(i.PROD_MAX*(-1)*i.activite for i in ville.equipConso) # Consommation totale pour l'étape en cours"""
    simulations = [i.simulation() for i in ville.equipProduction] #liste représentant les equipements de production pour l'etape suivante

    prod_actuelle = sum(i.activite*i.PROD_MAX for i in ville.equipProduction)
    conso_future = sum(i.activite*i.PROD_MAX for i in ville.equipConso)

    diff=conso_future-prod_actuelle # différence conso-production actuelle
    consigne = [i.activite for i in ville.equipProduction] # liste des consignes equipements de production
    
    consigne_stock=[i.activite for i in ville.equipStockage] # "" de stockage
    simulations_stock=[i.simulation() for i in ville.equipStockage]
    
    consigne_conso=[0 for i in range(ville.nombreEquipementConso)] # "" de consommation
    simulations_conso=[i.simulation() for i in ville.equipConso]

    if diff > 0: #on consommera plus qu'on ne produit
        max=sum(i.simulation()[1]*i.PROD_MAX for i in ville.equipProduction) #capacite de production maximale à l'etat suivant

        if max >= conso_future: # si on peut atteindre la valeur de la consommation...
            prod_provisoire = prod_actuelle

            while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire < conso_future): #tant que ecart > 2% ou prod > conso
                ind = ind_eqpascher(simulations,consigne) #indice de l'equipement le moins cher qu'on met au max
                equip = ville.equipProduction[ind]
                
                if (simulations[ind][0] < simulations[ind][1]):
                    while (prod_provisoire < conso_future and consigne[ind] < simulations[ind][1]):
                        consigne[ind] += (simulations[ind][1]-equip.activite)/10 #...on le met progressivement au max
                        prod_provisoire += (simulations[ind][1]-equip.activite)/10*equip.PROD_MAX #maj
                else:
                    consigne[ind] = simulations[ind][1]
                    prod_provisoire = prod_provisoire - equip.activite*equip.PROD_MAX + simulations[ind][1]*equip.PROD_MAX #maj

        else:
            for i in range (len(simulations)): # on met tout au max
                consigne[i] = simulations[i][1]
            prod_provisoire = sum(simulations[i][1]*ville.equipProduction[i].PROD_MAX for i in range(len(simulations)))

            # il faut maintenant compenser la différence prod-conso avec de l'effacement et du stockage
            stock_max = [simulations_stock[i][1] for i in range(len(consigne_stock))]
            while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire < conso_future and consigne_stock != stock_max):
                ind = ind_eqpascher(simulations_stock,consigne_stock)
                while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire < conso_future and consigne_stock[ind] != stock_max[ind]):
                    consigne_stock[ind] += (stock_max[ind] - ville.equipStockage[ind].activite)/10
                    prod_provisoire += (stock_max[ind] - ville.equipStockage[ind].activite)/10*ville.equipStockage[ind].PROD_MAX
                
            
            eff_max = [simulations_conso[i][1] for i in range(ville.nombreEquipementConso)]
            if consigne_stock==stock_max :
                while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire < conso_future and consigne_conso != eff_max):
                    ind = ind_eqpascher(simulations_conso, consigne_conso)
                    equip = ville.equipConso[ind]
                    consigne_conso[ind] = simulations_conso[ind][1]
                    conso_future -= (simulations_conso[ind][1]-simulations_conso[ind][1])*equip.PROD_MAX #on retire à conso_future l'effacement
                    
    else:
        min=sum(simulations[i][0] for i in range(len(simulations)))

        if min<=conso_future: # si on peut atteindre la valeur de la consommation...
            prod_provisoire = prod_actuelle

            while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire > conso_future): #tant que ecart > 2% ou prod > conso
                ind = ind_eqpascher(simulations,consigne) #indice de l'equipement le moins cher qu'on met au max
                equip = ville.equipProduction[ind]
                
                if (simulations[ind][0] < simulations[ind][1]):
                    while (prod_provisoire > conso_future and consigne[ind] > simulations[ind][0]):
                        consigne[ind] += (simulations[ind][0]-equip.activite)/10 #...on le met progressivement au max
                        prod_provisoire += (simulations[ind][0]-equip.activite)/10*equip.PROD_MAX #maj
                else:
                    consigne[ind] = simulations[ind][0]
                    prod_provisoire = prod_provisoire - equip.activite*equip.PROD_MAX + simulations[ind][0]*equip.PROD_MAX #max
        else:
            for i in range (len(simulations)): # on met tout au max
                consigne[i] = simulations[i][0]
            prod_provisoire = sum(simulations[i][0]*ville.equipProduction[i].PROD_MAX for i in range(len(simulations)))

            # il faut maintenant compenser la différence prod-conso avec de l'effacement et du stockage
            stock_min = [0. for i in range(len(consigne_stock))]
            while (abs(prod_provisoire-conso_future)/conso_future > 2./100 and prod_provisoire > conso_future and consigne_stock != stock_min):
                ind = ind_eqpascher(simulations_stock,consigne_stock)
                consigne_stock[ind]=0.
                prod_provisoire-=ville.equipStockage[ind].PROD_MAX
            

    for i in ville.equipConso:
        i.etatSuivant(100,0)
    for i in ville.equipProduction:
        i.etatSuivant(100,0)
    Global.db.enregistrerEtape(ville.equipProduction, ville.equipConso, 0)        
    Global.tempsinc()#temps+=1
    print Global.temps
    

print "ok!"
