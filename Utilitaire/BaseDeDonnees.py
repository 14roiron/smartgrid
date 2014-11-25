# -*- coding: utf-8 -*-

import MySQLdb

class BaseDeDonnees:
        
    def __init__(self):
        self.database = MySQLdb.connect(host="localhost", user = "root", passwd = "migse", db = "Smartgrid1")
    
    def importerTable(self, nom):
        cur = self.database.cursor()
        l = []
        cur.execute("SELECT * FROM " + nom)
        for row in cur.fetchall():
            dico = {"GHI":row[0], "DNI":row[1], "DHI":row[2], "T":row[3],\
                    "windSpeed":float(row[5]), "windGust":float(row[7]), "id":row[8]}
            l.append(dico)
        return l
