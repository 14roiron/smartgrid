# -*-coding:utf-8 -
import MySQLdb
import matplotlib.pyplot as plt
from Ville import Ville
from Utilitaire.heure import Utilitaire
#from numpy import where
from Utilitaire import Global
#from mercurial.util import interpolate

#nécéssite matplotlib!!!!

#assert __name__ == '__main__'

numtest=Global.numtest
#pas pour l'affichage des légendes

export=True
affichage=False
database = MySQLdb.connect(host="localhost", user = "root", passwd = "migse", db = "Smartgrid1")
cur = database.cursor()
#quelle est la durée de l'expérience?
cur.execute("""SELECT count( * )
FROM `Etat`
WHERE (numTest=\"{}\" AND IDObjet=0)""".format(numtest))

nb=int(cur.fetchall()[0][0])
pas=nb/12
#on génère un dico des IDs
ID = [] 
cur.execute("SELECT * FROM ID WHERE numTest=\"{}\"".format(numtest))
for row in cur.fetchall():
    dico = {"nom":row[2], "Pmax":float(row[3]), "Emax":float(row[4])}
    ID.append(dico)

#on génère deux listes de listes
#on a une liste (etat) correspondant à la consommation à chaque instant t de chaque équipement i
# et une correspondant à l'effacement

etat=[[] for i in range(nb)]
effacement = [[] for i in range(nb)]

for i in range(len(ID)):
    cur.execute("SELECT * FROM Etat WHERE (numTest=\"{}\" AND IDObjet={}) ORDER BY `Etat`.`t`".format(numtest,i))
    j=0
    for row in cur.fetchall():
        etat[j].append(row[3])
        effacement[j].append(row[4]) 
        j+=1

        
#liste des consignes
cur.execute("""SELECT count( * )
FROM `consigne`
WHERE (numTest=\"{}\" AND IDObjet=0)""".format(numtest))
nb=int(cur.fetchall()[0][0])
consigne=[[] for i in range(nb)]
for i in range(len(ID)):
    cur.execute("SELECT * FROM consigne WHERE (numTest=\"{}\" AND IDObjet={}) ORDER BY `consigne`.`t` ASC ".format(numtest,i))
    j=0
    for row in cur.fetchall():
        consigne[j].append(row[3]) 
        j+=1
#print len(etat)
#print len(consigne)

#on a besoin de séparer les consos/prods/stocks
Global.temps=0
ville=Ville()

abscissea=list(range(len(etat)))
abscisseb=["J{}:H{}".format(Utilitaire.calculDate(i)["Jour"],Utilitaire.calculDate(i)["Heure"]) if (i%pas == 0) else "" for i in range(len(etat))]
color=["blue","green","red","cyan","magenta","yellow"]
#génération des graphs individuels:
#je vais expliquer le premier les autres sont identique, soit ils concernent d'autre objets soit on ne sépare pas les graphs
#on génère une suite d'objets plot et dans chaque plot on génère deux liste, celle des instants t list(range(len(Etat)) 
#et une liste des conso [...] sisi ça marche relis bien la méthode
f,a=plt.subplots(ville.nombreEquipementProduction,sharex=True)
for i in range(ville.nombreEquipementProduction):
    l=a[i].plot(list(range(len(etat))), [etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], "r", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[i].get_legend_handles_labels()
    a[i].legend(handles, labels)  
    a[i].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,15)
    f.savefig('resultats/{}_Productions_individuelles.png'.format(numtest), bbox_inches='tight')


f,a=plt.subplots(ville.nombreEquipementConso, sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    a[k].plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,15)
    f.savefig('resultats/{}_Consommations_individuelles.png'.format(numtest), bbox_inches='tight')


"""
f,a=plt.subplots(ville.nombreEquipementStockage, sharex=True)
a=[a,]
for k in range(ville.nombreEquipementStockage):
    i=k+ville.nombreEquipementProduction+ville.nombreEquipementConso
    a[k].plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("stockage")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,15)
    f.savefig('resultats/{}_graphNum{}IndivStockage.png'.format(numtest), bbox_inches='tight')

"""
#tous sur le même graphe
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementProduction):
    a.plot(list(range(len(etat))), [etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Productions_individuelles(1graphe).png'.format(numtest), bbox_inches='tight')

          
f,a=plt.subplots(sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    a.plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Consommations_individuelles(1graphe).png'.format(numtest), bbox_inches='tight')


"""

f,a=plt.subplots(sharex=True)
for k in range(ville.nombreEquipementStockage):
    i=k+ville.nombreEquipementProduction+ville.nombreEquipementConso
    a.plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("Stockage")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_graphNum{}UniStockage.png'.format(numtest), bbox_inches='tight')

"""
#tous sur le même graphe en ajout
color={"turb":"blue","PVme":"green","eoli":"red","Mais":"cyan","Usin":"magenta","hopi":"yellow","ecla":"blue","maga":"green","Parc":"red","Stoc":"cyan"}
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementProduction):
    y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i+1)]) for j in range(len(etat))]
    y0=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[i]["nom"].decode('unicode-escape'),color=color[ID[i]["nom"][:4]])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[ID[i]["nom"][:4]], interpolate=True)
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Production_totale.png'.format(numtest), bbox_inches='tight')


f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementConso):
    k=i+ville.nombreEquipementProduction
    b=ville.nombreEquipementProduction
    y1=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k+1)]) for j in range(len(etat))]
    y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[k]["nom"].decode('unicode-escape'),color=color[ID[k]["nom"][:4]])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[ID[k]["nom"][:4]])
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Consommation_totale.png'.format(numtest), bbox_inches='tight')


# Production + stockage et consommation

f,a=plt.subplots(sharex=True)
nbProd = ville.nombreEquipementProduction
nbConso = ville.nombreEquipementConso
nbStock = ville.nombreEquipementStockage

for i in range(ville.nombreEquipementProduction):  # Production
    y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i+1)]) +\
        sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd+nbConso,nbProd+nbConso+nbStock)]) for j in range(len(etat))]
    y0=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i)]) +\
        sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd+nbConso,nbProd+nbConso+nbStock)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[i]["nom"].decode('unicode-escape'),color=color[ID[i]["nom"][:4]])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[ID[i]["nom"][:4]], interpolate=True)
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))

for i in range(nbStock):   # Stockage
    y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd+nbConso, nbProd+nbConso+i+1)]) for j in range(len(etat))]
        #sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd)]) for j in range(len(etat))]
    y0=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd+nbConso, nbProd+nbConso+i)])  for j in range(len(etat))]
        #sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[nbProd+nbConso+i]["nom"].decode('unicode-escape'),color=color[ID[nbProd+nbConso+i]["nom"][:4]])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[ID[nbProd+nbConso+i]["nom"][:4]], interpolate=True)
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))

y2=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(nbProd, nbProd + nbConso)]) for j in range(len(etat))]  # Consommation
a.plot(list(range(len(etat))), y2, linewidth=5, label="Consommation",color='k', linestyle='dashed')
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("Production + stockage et consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Somme_productions_stockages_et_consommation.png'.format(numtest), bbox_inches='tight')

"""
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementConso):
    k=i+ville.nombreEquipementProduction+ville.nombreEquipementConso
    b=ville.nombreEquipementProduction+ville.nombreEquipementConso
    y1=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k+1)]) for j in range(len(etat))]
    y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[k]["nom"].decode('unicode-escape'),color=color[ID[i]["nom"][:4]])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[ID[i]["nom"][:4]])
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("Stockage")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_graphNum{}SommeStock.png'.format(numtest), bbox_inches='tight')

"""
color=["blue","green","red","cyan","magenta","yellow"]
#affichage de la différence:
f,a=plt.subplots(sharex=True)
c=ville.nombreEquipementConso
b=ville.nombreEquipementProduction
y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(b)]) for j in range(len(etat))]
y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,b+c)]) for j in range(len(etat))]
a.plot(list(range(len(etat))), y1, linewidth=1, label="production",color=color[1%6])
a.plot(list(range(len(etat))), y0, linewidth=1, label="conso",color=color[2%6])
a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6],interpolate=True)
#a.fill_between(list(range(len(etat))),y0,y1,where=y0>y1,facecolor=color[4%6])
handles, labels = a.get_legend_handles_labels()
a.legend(handles, labels)  
a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("difference")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Production_et_consommation_totales.png'.format(numtest), bbox_inches='tight')
    

# Affichage du stockage ajouté à la production et de la consommation

f,a=plt.subplots(sharex=True)
c=ville.nombreEquipementConso
b=ville.nombreEquipementProduction
stock = ville.nombreEquipementStockage
y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(b)]) +\
    sum([etat[j][st]*ID[st]["Pmax"]/100. for st in range(b+c, b+c+stock)]) for j in range(len(etat))]
y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,b+c)]) for j in range(len(etat))]
a.plot(list(range(len(etat))), y1, linewidth=1, label="production et stockage",color=color[1%6])
a.plot(list(range(len(etat))), y0, linewidth=1, label="conso",color=color[2%6])
a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6],interpolate=True)
#a.fill_between(list(range(len(etat))),y0,y1,where=y0>y1,facecolor=color[4%6])
handles, labels = a.get_legend_handles_labels()
a.legend(handles, labels)  
a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("difference")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Production+stockage_et_consommation_totales.png'.format(numtest), bbox_inches='tight')



#affichage de la différence en mode somme:
f,a=plt.subplots(sharex=True)
c=ville.nombreEquipementConso
b=ville.nombreEquipementProduction
d=ville.nombreEquipementStockage
y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(c+d+b)]) for j in range(len(etat))]
a.plot(list(range(len(etat))), y1, linewidth=1, label="difference",color=color[1%6])
handles, labels = a.get_legend_handles_labels()
a.legend(handles, labels)  
a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("difference")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/{}_Difference_production_consommation.png'.format(numtest), bbox_inches='tight')


#affichage des consignes en pourcents:
f,a=plt.subplots(ville.nombreEquipementProduction,sharex=True)
for i in range(ville.nombreEquipementProduction):#en %.. *ID[i]["Pmax"]/100. pour les puissances
    a[i].plot(list(range(len(etat))), [consigne[j][i] for j in range(len(consigne))], "r", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[i].get_legend_handles_labels()
    a[i].legend(handles, labels)  
    a[i].axis(xmin=0, xmax=len(etat))
plt.ylabel("consignes %")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementProduction)
    f.savefig('resultats/{}_Consignes_individuelles_de_production.png'.format(numtest), bbox_inches='tight')

#consignes de conso:
f,a=plt.subplots(ville.nombreEquipementConso, sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction#en %*ID[i]["Pmax"]/100.
    a[k].plot(list(range(len(etat))), [-consigne[j][i] for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("consigne %")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementConso)
    f.savefig('resultats/{}_Consignes_individuelles_de_consommation.png'.format(numtest), bbox_inches='tight')


f,a=plt.subplots(ville.nombreEquipementStockage, sharex=True)
#a=[a,]
for k in range(ville.nombreEquipementStockage):
    i=k+ville.nombreEquipementProduction+ville.nombreEquipementConso#*ID[i]["Pmax"]/100.
    a[k].plot(list(range(len(etat))), [consigne[j][i] for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("consignes %")
plt.xlabel('Temps')
plt.title("stockage")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementStockage)
    f.savefig('resultats/{}_Consignes_individuelles_de_stockage.png'.format(numtest), bbox_inches='tight')


#différence consignes 

#affichage des consignes en pourcents:
f,a=plt.subplots(ville.nombreEquipementProduction,sharex=True)
for i in range(ville.nombreEquipementProduction):#en %.. *ID[i]["Pmax"]/100. pour les puissances
    y0=[consigne[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    y1=[etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    a[i].plot(list(range(len(etat))),y0, "r", linewidth=1, color=color[1%6],label="consigne {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[i].plot(list(range(len(etat))), y1, "r", linewidth=1, color=color[2%6],label="Prod {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[i].fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6])
    handles, labels = a[i].get_legend_handles_labels()
    a[i].legend(handles, labels)  
    a[i].axis(xmin=0, xmax=len(etat))
plt.ylabel("Differences consignes Prod kW")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementProduction)
    f.savefig('resultats/{}_Ecart_consigne_production.png'.format(numtest), bbox_inches='tight')

#consignes de conso:
f,a=plt.subplots(ville.nombreEquipementConso, sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction#en %*ID[i]["Pmax"]/100.
    y0=[consigne[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    y1=[etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    a[k].plot(list(range(len(etat))),y0, "r", linewidth=1,color=color[1%6], label="consigne {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[k].plot(list(range(len(etat))), y1, "r", linewidth=1,color=color[2%6], label="Prod {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[k].fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6])
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("Difference Consigne/Conso kW")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementConso)
    f.savefig('resultats/{}_Ecart_consigne_consommation.png'.format(numtest), bbox_inches='tight')


f,a=plt.subplots(ville.nombreEquipementStockage, sharex=True)
#a=[a,]
for k in range(ville.nombreEquipementStockage):
    i=k+ville.nombreEquipementProduction+ville.nombreEquipementConso#*ID[i]["Pmax"]/100.
    y0=[consigne[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    y1=[etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))]
    a[k].plot(list(range(len(etat))),y0, "r", linewidth=1,color=color[1%6], label="consigne {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[k].plot(list(range(len(etat))), y1, "r", linewidth=1,color=color[2%6], label="Prod {}".format(ID[i]["nom"]).decode('unicode-escape'))
    a[k].fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6])
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("Difference Consigne/Conso kW")
plt.xlabel('Temps')
plt.title("consommation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,3*ville.nombreEquipementStockage)
    f.savefig('resultats/{}_Ecart_stockage_consigne.png'.format(numtest), bbox_inches='tight')

# Capacité de stockage restante

f,a=plt.subplots(ville.nombreEquipementStockage, sharex=True)
for k in range(ville.nombreEquipementStockage):
    i = k + ville.nombreEquipementProduction + ville.nombreEquipementConso
    a[k].plot(list(range(len(etat))), [effacement[j][i] for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("Stockage dispo kW.h")
plt.xlabel('Temps')
plt.title("Stockage disponible")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(15,15)
    f.savefig('resultats/{}_Stockage_restant(individuel).png'.format(numtest), bbox_inches='tight')

# Coût





#différence consignes 

if affichage==True:
    plt.show()



print "ok"
