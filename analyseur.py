# -*-coding:utf-8 -
import MySQLdb
import matplotlib.pyplot as plt
from Ville import Ville
from Utilitaire.heure import Utilitaire
from numpy import where

#nécéssite matplotlib!!!!

assert __name__ == '__main__'

numtest=1
#pas pour l'affichage des légendes
pas=2*6#6H
export=True
affichage=False

database = MySQLdb.connect(host="localhost", user = "root", passwd = "migse", db = "Smartgrid1")
cur = database.cursor()

#on génère un dico des IDs
ID = [] 
cur.execute("SELECT * FROM ID WHERE numTest={}".format(numtest))
for row in cur.fetchall():
    dico = {"nom":row[2], "Pmax":float(row[3]), "Emax":float(row[4])}
    ID.append(dico)

#on génère une liste de liste
#on a une liste correspondant à la consommation à chaque instant t de chaque équipement i
cur.execute("""SELECT count( * )
FROM `Etat`
WHERE (numTest={} AND IDObjet=0)""".format(numtest))
nb=int(cur.fetchall()[0][0])
etat=[[] for i in range(nb)]
for i in range(len(ID)):
    cur.execute("SELECT * FROM Etat WHERE (numTest={} AND IDObjet={}) ORDER BY `Etat`.`t`".format(numtest,i))
    j=0
    for row in cur.fetchall():
        etat[j].append(row[3]) 
        j+=1

#on a besoin de séparer les consos/prods/stocks
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
    f.set_size_inches(13,7)
    f.savefig('resultats/graphIndivProdNum{}.png'.format(numtest), bbox_inches='tight')

f,a=plt.subplots(ville.nombreEquipementConso, sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    a[k].plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consomation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphIndivConsoNum{}.png'.format(numtest), bbox_inches='tight')


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
    f.set_size_inches(13,7)
    f.savefig('resultats/graphIndivStockageNum{}.png'.format(numtest), bbox_inches='tight')

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
    f.savefig('resultats/graphUniProdNum{}.png'.format(numtest), bbox_inches='tight')

          
f,a=plt.subplots(sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    a.plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"]/100. for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consomation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphUniConsoNum{}.png'.format(numtest), bbox_inches='tight')


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
    f.savefig('resultats/graphUniStockageNum{}.png'.format(numtest), bbox_inches='tight')

"""
#tous sur le même graphe en ajout
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementProduction):
    y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i+1)]) for j in range(len(etat))]
    y0=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(i)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[i]["nom"].decode('unicode-escape'),color=color[i%6])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[i%6], interpolate=True)
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphSommeProdNum{}.png'.format(numtest), bbox_inches='tight')



f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementConso):
    k=i+ville.nombreEquipementProduction
    b=ville.nombreEquipementProduction
    y1=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k+1)]) for j in range(len(etat))]
    y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[k]["nom"].decode('unicode-escape'),color=color[i%6])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[i%6])
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("Consomation")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphSommeConsoNum{}.png'.format(numtest), bbox_inches='tight')

"""
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementConso):
    k=i+ville.nombreEquipementProduction+ville.nombreEquipementConso
    b=ville.nombreEquipementProduction+ville.nombreEquipementConso
    y1=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k+1)]) for j in range(len(etat))]
    y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,k)]) for j in range(len(etat))]
    a.plot(list(range(len(etat))), y1, linewidth=1, label=ID[k]["nom"].decode('unicode-escape'),color=color[i%6])
    a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[i%6])
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("Stockage")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphSommeStockNum{}.png'.format(numtest), bbox_inches='tight')

"""

#affichage de la différence:
f,a=plt.subplots(sharex=True)
c=ville.nombreEquipementConso
b=ville.nombreEquipementProduction
y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(b)]) for j in range(len(etat))]
y0=[sum([-etat[j][l]*ID[l]["Pmax"]/100. for l in range(b,b+c)]) for j in range(len(etat))]
a.plot(list(range(len(etat))), y0, linewidth=1, label="production",color=color[1%6])
a.plot(list(range(len(etat))), y1, linewidth=1, label="conso",color=color[2%6])
a.fill_between(list(range(len(etat))),y0,y1,facecolor=color[3%6])
handles, labels = a.get_legend_handles_labels()
a.legend(handles, labels)  
a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("difference")
plt.xticks(abscissea,abscisseb)
if export==True:
    f.set_size_inches(13,7)
    f.savefig('resultats/graphDifferenceCNum{}.png'.format(numtest), bbox_inches='tight')




#affichage de la différence en mode somme:
f,a=plt.subplots(sharex=True)
c=ville.nombreEquipementConso
b=ville.nombreEquipementProduction
y1=[sum([etat[j][l]*ID[l]["Pmax"]/100. for l in range(c+b)]) for j in range(len(etat))]
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
    f.savefig('resultats/graphDifferenceNum{}.png'.format(numtest), bbox_inches='tight')


if affichage==True:
    plt.show()



print "ok"
