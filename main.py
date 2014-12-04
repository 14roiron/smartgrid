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
from Utilitaire import Global
import sys


"""Import de la base de données"""

#commande main.py duree=24*6 nomdutest=0 datededébut=0
analyseur=True
if( len(sys.argv)>1):
    Global.duree=eval(sys.argv[1])
    analyseur=True
if(len(sys.argv)>2):
    Global.numtest=sys.argv[2]
if(len(sys.argv)>3):
    Global.temps=eval(sys.argv[3])
"""initialisation de la Ville dans l'objet Ville"""
ville = Ville()
numTest = Global.numtest
Global.duree += Global.temps #décalage si présence d'un offset
duree = Global.duree
    


def ind_eqpascher(liste,consigne): #pour prod MAX !! indice de l'equipement le moins cher, liste comme simulations
    i=0
    while (i < len(liste) and abs(consigne[i] - liste[i][1]) < 10.**(-3)): #indice d'un équipement pas encore au max
        i+=1
    if i < len(liste):
        cout_min = liste[i][4]
        for j in range (0,len(liste)):
            if (liste[j][4] < cout_min and abs(consigne[j] - liste[j][1]) > 10.**(-3)): #si moins cher et pas encore mis au max
                i=j
        return i
    else:
        return i


def ind_eqpascher2(liste,consigne): #pour prod MAX !! indice de l'equipement le moins cher, liste comme simulations
    i=0
    while (i < len(liste) and abs(consigne[i] - liste[i][0]) < 10.**(-3)): #indice d'un équipement pas encore au max
        i+=1
    if i < len(liste):
        cout_min = liste[i][2]
        for j in range (0,len(liste)):
            if (liste[j][2] < cout_min and abs(consigne[j] - liste[j][0]) > 10.**(-3)): #si moins cher et pas encore mis au max
                i=j
        return i
    else:
        return i

Global.db.vide_table(numTest)
Global.db.enregistrerID(ville.equipProduction, ville.equipConso, ville.equipStockage, numTest)
Global.db.enregistrerEtape(ville.equipProduction, ville.equipConso, ville.equipStockage, numTest)
Global.db.enregistrerConsigne([0 for i in range(ville.nombreEquipementProduction)], [0 for i in range(ville.nombreEquipementConso)],[0 for i in range(ville.nombreEquipementStockage)], numTest) 

while Global.temps < duree-1: #boucle principale
    prod_actuelle = sum(i.prevision()[0]/100.*i.PROD_MAX for i in ville.equipProduction)
    conso_future = sum(-i.production[Global.temps + 1]/100.*i.PROD_MAX for i in ville.equipConso)

    diff = conso_future-prod_actuelle # différence conso-production actuelle
    #print "diff : %s" %diff
    effacement_actuel = 0.
    
    consigne = [i.prevision()[0] for i in ville.equipProduction] # liste des consignes equipements de production
    simulations = [i.simulation() for i in ville.equipProduction] #liste représentant les equipements de production pour l'etape suivante
    
    consigne_stock = [0 for i in ville.equipStockage] # "" de stockage
    simulations_stock=[i.simulation() for i in ville.equipStockage]
    
    consigne_conso = [0. for i in range(len(ville.equipConso))] # "" de consommation étalonné sans effacement
    simulations_conso = [i.simulation() for i in ville.equipConso] 
    if diff > 0.: #on consommera plus qu'on ne produit
        max = sum(i.simulation()[1]/100.*i.PROD_MAX for i in ville.equipProduction) #capacite de production maximale à l'etat suivant
        #print "max : %s" %max
        #print "conso future : %s" %conso_future
        if max >= conso_future: # si on peut atteindre la valeur de la consommation...
            """for i in ville.equipProduction:
                print i.nom
                print i.prevision()[0]
		"""
            #print [i.prevision()[0]/100.*i.PROD_MAX for i in ville.equipProduction]   
            prod_provisoire =  sum(i.prevision()[0]/100.*i.PROD_MAX for i in ville.equipProduction)
            
            ind_boucle = len(ville.equipProduction) #pour éviter les boucles infinies
            while (abs(prod_provisoire-conso_future) > 2./100.*conso_future and prod_provisoire < conso_future and ind_boucle > 0): #tant que ecart > 2% et prod < conso
                ind = ind_eqpascher(simulations,consigne) #indice de l'equipement le moins cher qu'on met au max
                if ind < len(ville.equipProduction):
                    equip = ville.equipProduction[ind]
                    ind_boucle -= 1               
                
                    if (simulations[ind][0] < simulations[ind][1]): #équipement à production laissant marge de maneuvre ex : centrale (et pas PV)
                        ind_boucle3 = 100 #boucle de sécurité 
                        while (prod_provisoire < conso_future and abs(consigne[ind] - simulations[ind][1]) > 10.**(-4) and ind_boucle3 > 0):
                            consigne[ind] += (simulations[ind][1]-equip.activite)/100. #on met progressivement la production au max
                            prod_provisoire += (simulations[ind][1]-equip.activite)/100./100.*equip.PROD_MAX #maj
                            ind_boucle3 -=1
                        
                       
                    else:
                        consigne[ind] = simulations[ind][1] #sinon on met à la production min = max (on n'a pas le choix)
                        prod_provisoire += (simulations[ind][1]- equip.activite)/100.*equip.PROD_MAX #maj                
                else:
                     print "indice équipement quand max > conso_future récupéré de ind_pascher trop grand"
                     break
        else: #on n'a pas suffisamment de production disponible
            for i in range (len(simulations)): # on met tout au max
                consigne[i] = simulations[i][1]
            prod_provisoire = sum(simulations[i][1]/100.*ville.equipProduction[i].PROD_MAX for i in range(len(simulations)))
            
            # il faut maintenant compenser la différence prod-conso avec du stockage et eventuellement de l'effacement
            #print "Début stockage"
            stock_max = [simulations_stock[i][1] for i in range(len(simulations_stock))] #tous les stockages sont en mode "vidage maximal"

            ind_boucle2 = len(ville.equipStockage)
            while (abs(prod_provisoire-conso_future)/conso_future > 2./100. and prod_provisoire < conso_future and abs(sum(consigne_stock) - sum(stock_max)) >= sum(stock_max)*0.05\
            and ind_boucle2 > 0):
                ind = ind_eqpascher(simulations_stock,consigne_stock) #stockage le moins cher à vider
                if ind < len(ville.equipStockage):
                    equip = ville.equipStockage[ind]
		    consigne_ind = consigne_stock[ind]
                    ind_boucle2 -= 1

                    ind_boucle = 10
                    while (abs(prod_provisoire-conso_future)/conso_future > 2./100. and prod_provisoire < conso_future and abs(consigne_stock[ind] - stock_max[ind]) > 10.**(-3) and ind_boucle > 0):
                        consigne_stock[ind] += (simulations_stock[ind][1] - consigne_ind)/10.
                        prod_provisoire += (simulations_stock[ind][1] - consigne_ind)/100./10.*equip.PROD_MAX
                        ind_boucle -= 1
                        #print "vidage progressif, étape : %s" %ind_boucle
                        
                    if consigne_stock[ind] < 10**(-3):
                        consigne_stock[ind] = 0.
                else:
                    print "indice stockage récupéré par ind_pascher trop grand"
                    break        

            conso_min = [(i.simulation()[1]-i.activite)*(i.PROD_MAX)/i.EFFA_MAX for i in ville.equipConso]
            '''production = - consommation ; 
               prod_min = - conso_max = conso sans effacement ;
               prod_max = - conso_min = conso avec effacement ; => cout_max = cout pour effacer
               effacement = prod_max - prod_min 
               attention prod_min  = -conso
            '''
            if (abs(sum(stock_max)-sum(consigne_stock)) <= 10.**(-3)): #tout le stockage est au max
                ind_boucle = len(ville.equipConso) #boucle de sécurité
                #print "Début effacement"
                #print "Conso_future avant effacement : %s" %conso_future
                while (abs(prod_provisoire-conso_future) > 2./100.*conso_future and prod_provisoire < conso_future and abs(sum(consigne_conso) - sum(conso_min)) > sum(conso_min)*0.05 and ind_boucle >0):
                    ind = ind_eqpascher(simulations_conso, consigne_conso)
                    ind_boucle -= 1
                    if ind < len(ville.equipConso):
                        equip = ville.equipConso[ind]
                        consigne_conso[ind] = (simulations_conso[ind][1]-equip.activite)*(equip.PROD_MAX)/equip.EFFA_MAX #attention cette consigne est un effacement
                        effacement_actuel += (simulations_conso[ind][1]-equip.activite)/100.*equip.PROD_MAX
                        conso_future -= (simulations_conso[ind][1]-equip.activite)/100.*(equip.PROD_MAX) #on retire à conso_future l'effacement
                    else:
                        print "indice effacement récupéré par ind_pascher trop grand"
                        break
                #print "Conso_future après effacement : %s" %conso_future
    else:
        
        min = sum(i.simulation()[0]/100.*i.PROD_MAX for i in ville.equipProduction) #capacite de production minimale à l'etat suivant
        #print "min : %s" %min
        #print "conso future : %s" %conso_future

        if min <= conso_future: # si on peut atteindre la valeur de la consommation...
            prod_provisoire = prod_actuelle
	    for i in range(len(ville.equipStockage)): #cette boucle a pour but de recharger les stockages à 50% de leur capacité
		equip = ville.equipStockage[i]
		if equip.reste < equip.capacite/2.:
		    ind_boucle=10
		    while (conso_future<prod_provisoire and ind_boucle<10):
		        consigne_stock[i]=(equip.reste-equip.capacite/2.)/equip.PROD_MAX*60.
		        prod_provisoire-=(equip.capacite/2.-equip.reste)*0.6
			ind_boucle-=1
            print [i.reste for i in ville.equipStockage]
            ind_boucle4 = len(ville.equipProduction) #boucle de sécurité
            while (abs(prod_provisoire-conso_future) > 10.**(-3) and prod_provisoire > conso_future and ind_boucle4 > 0): #tant que ecart > 2% et prod > conso
                ind = ind_eqpascher2(simulations,consigne) #indice de l'equipement le moins cher qu'on met au min
                if ind < len(ville.equipProduction):
                    equip = ville.equipProduction[ind]
                    ind_boucle4 -= 1
                    if (simulations[ind][0] < simulations[ind][1]): #equipement à production laissant marge de maneuvre ex : centrale (et pas PV)
                        ind_boucle5 = 100
                        while (prod_provisoire > conso_future and abs(consigne[ind]-simulations[ind][0]) >= simulations[ind][0]*0.005 and ind_boucle5 > 0):
                            consigne[ind] -= (equip.activite-simulations[ind][0])/100. #on met progressivement la production au min
                            prod_provisoire -= (equip.activite-simulations[ind][0])/100./100.*equip.PROD_MAX #maj
                            ind_boucle5 -= 1
                    else:
                        consigne[ind] = simulations[ind][0] #sinon on met à la production min = max (on n'a pas le choix)
                        prod_provisoire -= (equip.activite-simulations[ind][0])/100.*equip.PROD_MAX #maj
                else:
                    print "indice équipement quand min < conso_future récupéré de ind_pascher trop grand"
                    break  

        else: #on ne peut pas baisser suffisamment la production
            for i in range (len(simulations)): # on met tout au min
                consigne[i] = simulations[i][0]
            prod_provisoire = sum(simulations[i][0]/100.*ville.equipProduction[i].PROD_MAX for i in range(len(simulations)))

            # il faut maintenant compenser la différence prod-conso avec du stockage
            #print "Début remplissage stockage"
            stock_min = [simulations_stock[i][0] for i in range(len(simulations_stock))] #tous les stockages sont en mode "remplissage maximal"
            while (abs(prod_provisoire-conso_future) > 2./100.*conso_future and prod_provisoire > conso_future and abs(sum(consigne_stock)-sum(stock_min)) >= 10.**(-3)):
                ind = ind_eqpascher2(simulations_stock,consigne_stock) #stockage le moins cher à remplir
                #print "stockage en cours"
                if ind < len(ville.equipStockage):
                    equip = ville.equipStockage[ind]
                    consigne_ind = consigne_stock[ind]
                    ind_boucle6 = len(ville.equipStockage)*10
                    while (abs(prod_provisoire-conso_future) > 2./100.*conso_future and prod_provisoire > conso_future and abs(consigne_stock[ind]-stock_min[ind]) >= stock_min[ind]*0.005 and ind_boucle6 > 0):
                        consigne_stock[ind] -= (consigne_ind - simulations_stock[ind][0])/100.
                        prod_provisoire -= (consigne_ind - simulations_stock[ind][0])/100./100.*equip.PROD_MAX
                        ind_boucle6 -= 1
                else:
                    print "indice stockage récupéré par ind_pascher trop grand"
                    break
                    
    stock_max=[i.simulation()[1] for i in ville.equipStockage]
    stock_min=[i.simulation()[0] for i in ville.equipStockage]
    while (abs(conso_future-prod_provisoire)>conso_future*0.005):# and abs(sum(consigne_stock) - sum(stock_max))>sum(stock_max)*0.05 and abs(sum(consigne_stock) - sum(stock_min))>abs(sum(stock_min))*0.05)
        if conso_future - prod_provisoire > 0.:
            if abs(sum(consigne_stock) - sum(stock_max))<sum(stock_max)*0.05:
                break
	    ind = ind_eqpascher(simulations_stock,consigne_stock) #stockage le moins cher à vider
            if ind < len(ville.equipStockage):
                equip = ville.equipStockage[ind]
		consigne_ind = consigne_stock[ind]
                ind_boucle = 100
                while (abs(prod_provisoire-conso_future)/conso_future > 0.005 and prod_provisoire < conso_future and abs(consigne_stock[ind] - stock_max[ind]) > 10.**(-3) and ind_boucle>0.):
                    consigne_stock[ind] += (simulations_stock[ind][1] - consigne_ind)/100.
                    prod_provisoire += (simulations_stock[ind][1] - consigne_ind)/100./100.*equip.PROD_MAX
                    ind_boucle -= 1
                    #print "vidage progressif, étape : %s" %ind_boucle
                        
                if consigne_stock[ind] < 10**(-3):
                    consigne_stock[ind] = 0.
	    else:
                break

	else:
            if abs(sum(consigne_stock) - sum(stock_min))<abs(sum(stock_min))*0.05:
                break
            ind = ind_eqpascher2(simulations_stock,consigne_stock) #stockage le moins cher à remplir
            if ind < len(ville.equipStockage):
                equip = ville.equipStockage[ind]
                consigne_ind = consigne_stock[ind]
                ind_boucle6 = len(ville.equipStockage)*10
                while (abs(prod_provisoire-conso_future) > 0.005*conso_future and prod_provisoire > conso_future and abs(consigne_stock[ind]-stock_min[ind]) >= stock_min[ind]*0.005 and ind_boucle6 > 0):
                    consigne_stock[ind] -= (consigne_ind - simulations_stock[ind][0])/100.
                    prod_provisoire -= (consigne_ind - simulations_stock[ind][0])/100./100.*equip.PROD_MAX
                    ind_boucle6 -= 1
	    else:
		break
		    
    ecart = conso_future-prod_provisoire # ecart qui sera de l'import/export
    if abs(ecart)>conso_future*0.02:
        print consigne_stock
    print ecart
    ville.equipProduction[0].effacement = ecart
    ''' print effacement_actuel'''
    '''envoie des consignes et effacements pour la prochaine étape :) '''

    for i in range(len(consigne)):
       
        ville.equipProduction[i].etatSuivant(consigne[i],0.)
    
    for i in range(len(consigne_stock)):
       
        ville.equipStockage[i].etatSuivant(consigne_stock[i],0.)
    
    for i in range(len(consigne_conso)):
        
        ville.equipConso[i].etatSuivant(0.,consigne_conso[i])

    print [i.reste for i in ville.equipStockage]
    
    Global.db.enregistrerConsigne(consigne, consigne_conso, consigne_stock, numTest)
    Global.db.enregistrerEtape(ville.equipProduction, ville.equipConso, ville.equipStockage, numTest)        
    Global.tempsinc()#temps+=1
    print "Etape : %s" %Global.temps
    

print "ok!"
if(analyseur):
    execfile("analyseur.py")
