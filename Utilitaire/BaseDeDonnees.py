# -*- coding: utf-8 -*-

import MySQLdb
from Utilitaire import Global

class BaseDeDonnees:
        
    def __init__(self):
        self.database = MySQLdb.connect(host="localhost", user = "root", passwd = "migse", db = "Smartgrid1")
    
    def importerMeteo(self, nom):
        cur = self.database.cursor()
        l = []
        cur.execute("SELECT * FROM " + nom)
        for row in cur.fetchall():
            dico = {"GHI":row[0], "DNI":row[1], "DHI":row[2], "T":row[3],\
                    "windSpeed":float(row[5]), "windGust":float(row[7]), "id":row[8]}
            l.append(dico)
        return l
    
    def enregistrerID(self, listeProd, listeConso, numTest):
        cur = self.database.cursor()
        IDObjet = 0
        liste = listeProd
        liste += listeConso
        for equipement in liste:
            sql = """INSERT INTO ID (IDObjet, Nom, Pmax, Emax, numTest)
                     VALUES (%s, %s, %s, %s, %s)"""
            try:
                cur.execute(sql, (IDObjet, equipement.Nom, equipement.PROD_MAX, equipement.EFFA_MAX, numTest))
                self.database.commit()
                IDObjet += 1
            except:
                self.database.rollback()
                print "Erreur d'insertion dans ID"
        cur.close()
    
    def enregistrerEtape(self, listeProd, listeConso, numTest):
        cur = self.database.cursor()
        IDObjet = 0
        liste = listeProd
        liste += listeConso
        for equipement in liste:
            sql = """INSERT INTO Etat (t, IDObjet, P, E, C, numTest)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                cur.execute(sql, (temps, IDObjet, equipement.activite, equipement.effacement, equipement.cout, numTest))
                self.database.commit()
                IDObjet += 1
            except:
                self.database.rollback()
                print "Erreur d'insertion dans Etat"
