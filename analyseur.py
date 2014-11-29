# -*-coding:utf-8 -
import MySQLdb
import matplotlib.pyplot as plt
from Ville import Ville
from Utilitaire import heure
assert __name__ == '__main__'
numtest=0

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
etat=[[] for i in range(6*24*7)]
for i in range(len(ID)):
    cur.execute("SELECT * FROM Etat WHERE (numTest={} AND IDObjet={}) ORDER BY `Etat`.`t`".format(numtest,i))
    j=0
    for row in cur.fetchall():
       etat[j].append(row[3]) 
       j+=1
       
#on a besoin de séparer les consos/prods/stocks
ville=Ville()

#génération des graphs individuels:
#je vais expliquer le premier les autres sont identique, soit ils concernent d'autre objets soit on ne sépare pas les graphs
#on génère une suite d'objets plot et dans chaque plot on génère deux liste, celle des instants t list(range(len(Etat)) 
#et une liste des conso [...] sisi ça marche relis bien la méthode
f,a=plt.subplots(ville.nombreEquipementProduction,sharex=True)
for i in range(ville.nombreEquipementProduction):
    l=a[i].plot(list(range(len(etat))), [etat[j][i]*ID[i]["Pmax"] for j in range(len(etat))], "r", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[i].get_legend_handles_labels()
    a[i].legend(handles, labels)  
    a[i].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")

f,a=plt.subplots(ville.nombreEquipementConso, sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    a[k].plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"] for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consomation")


f,a=plt.subplots(ville.nombreEquipementStockage, sharex=True)
a=[a,]
for k in range(ville.nombreEquipementStockage):
    i=k+ville.nombreEquipementProduction+ville.nombreEquipementConso
    a[k].plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"] for j in range(len(etat))], "b", linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a[k].get_legend_handles_labels()
    a[k].legend(handles, labels)  
    a[k].axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("stockage")

#tous sur le même graphe
f,a=plt.subplots(sharex=True)
for i in range(ville.nombreEquipementProduction):
    a.plot(list(range(len(etat))), [etat[j][i]*ID[i]["Pmax"] for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("production")
          
f,a=plt.subplots(sharex=True)
for k in range(ville.nombreEquipementConso):
    i=k+ville.nombreEquipementProduction
    print i
    a.plot(list(range(len(etat))), [-etat[j][i]*ID[i]["Pmax"] for j in range(len(etat))], linewidth=1, label=ID[i]["nom"].decode('unicode-escape'))
    handles, labels = a.get_legend_handles_labels()
    a.legend(handles, labels)  
    a.axis(xmin=0, xmax=len(etat))
plt.ylabel("puissance kW")
plt.xlabel('Temps')
plt.title("consomation")
          

plt.show()



print "ok"