# -*- coding: utf-8 -*-

import MySQLdb
import Global

class BaseDeDonnees:
          
    def __init__(self):
        self.database = MySQLdb.connect(host="localhost", user = "root", passwd = "migse", db = "Smartgrid1")
        self.cur = self.database.cursor()
        
    def importerMeteo(self, nom):
        #cur = self.database.cursor()
        l = []
        self.cur.execute("SELECT * FROM " + nom)
        for row in self.cur.fetchall():
            dico = {"GHI":row[0], "DNI":row[1], "DHI":row[2], "T":row[3],\
                    "windSpeed":float(row[5]), "windGust":float(row[7]), "id":row[8]}
            l.append(dico)
        return l
    
    def enregistrerID(self, listeProd, listeConso, listeStockage, numTest):
        #cur = self.database.cursor()
        IDObjet = 0
        liste = list(listeProd)
        liste += listeConso
        liste += listeStockage
        for equipement in liste:
            sql = """INSERT INTO ID (IDObjet, Nom, Pmax, Emax, numTest)
                     VALUES (%s, %s, %s, %s, %s)"""
            sql2 = """INSERT INTO ID (IDObjet, Nom, Pmax, Emax, numTest)
                     VALUES ({}, {}, {}, {}, {})"""
            try:
                self.cur.execute(sql, (IDObjet, equipement.nom, equipement.PROD_MAX, equipement.EFFA_MAX, numTest))
                #print sql2.format(IDObjet, equipement.nom, equipement.PROD_MAX, equipement.EFFA_MAX, numTest)
                self.database.commit()
                IDObjet += 1
            except Exception as e:
                self.database.rollback()
                print "Erreur d'insertion dans ID"
                print e
    
    def enregistrerEtape(self, listeProd, listeConso, listeStockage, numTest):
        
        IDObjet = 0
        liste = list(listeProd)
        liste += listeConso
        liste += listeStockage
        for equipement in liste:
            sql = """INSERT INTO Etat (t, IDObjet, P, E, C, numTest)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            try:
                self.cur.execute(sql, (Global.temps, IDObjet, equipement.activite, equipement.effacement, equipement.cout, numTest))
                self.database.commit()
                 #print sql % (Global.temps, IDObjet, equipement.activite, equipement.effacement, equipement.cout, numTest)
                IDObjet += 1
            except Exception as e:
                self.database.rollback()
                print "Erreur d'insertion dans Etat"
                print e
    def enregistrerConsigne(self, listeProd, listeConso, listeStockage, numTest):
        
        IDObjet = 0
        liste = list(listeProd)
        liste += listeConso
        liste += listeStockage
        for equipement in liste:
            sql = """INSERT INTO consigne (t, IDObjet, consigne, numTest)
                     VALUES (%s, %s, %s, %s)"""
            try:
                self.cur.execute(sql, (Global.temps, IDObjet, equipement, numTest))
                self.database.commit()
                #print sql % (Global.temps, IDObjet, equipement, numTest)
                IDObjet += 1
            except Exception as e:
                self.database.rollback()
                print "Erreur d'insertion dans Etat"
                print e
    def vide_table(self,numTest):
        sql = "DELETE FROM `Etat` WHERE `NumTest` =\"{}\" ".format(numTest)
        sql2 = "DELETE FROM ID WHERE `NumTest` =\"{}\"".format(numTest)
        sql3 = "DELETE FROM consigne` WHERE `NumTest` =\"{}\"".format(numTest)
        
        try:
            self.cur.execute(sql)
            self.database.commit()
            self.cur.execute(sql2)
            self.database.commit()
        except Exception as e:
            self.database.rollback()
            print "Erreur d'de vidage dans Etat"
            print e