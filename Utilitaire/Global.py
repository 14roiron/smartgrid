from BaseDeDonnees import BaseDeDonnees
temps=0
db = BaseDeDonnees()
meteo1 = db.importerMeteo("Semaine1")
meteo2 = db.importerMeteo("Semaine2")
meteoTest = db.importerMeteo("Test")
def tempsinc():
    global temps
    temps+=1
def gettemps():
    return temps
