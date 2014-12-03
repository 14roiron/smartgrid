from BaseDeDonnees import BaseDeDonnees
temps=0
numtest=0
duree=6*24

db = BaseDeDonnees()
meteo1 = db.importerMeteo("Semaine1")
meteo2 = db.importerMeteo("Semaine2")
meteo3 = db.importerMeteo("Semaine3")
meteo4 = db.importerMeteo("Semaine4")
meteo5 = db.importerMeteo("Semaine5")
meteoTest = db.importerMeteo("Test")
def tempsinc():
    global temps
    temps+=1
def gettemps():
    return temps
