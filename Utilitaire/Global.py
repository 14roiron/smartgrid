from Utilitaire.BaseDeDonnees import BaseDeDonnees
temps=0
db = BaseDeDonnees()
meteo1 = db.importerTable("Semaine1")
meteo2 = db.importerTable("Semaine2")
meteoTest = db.importerTable("Test")