class Utilitaire:
    
    def __init__ (self,temps):
        self.date = Utilitaire.calculDate(10*temps)
        self.temps=temps
        
    def calculDate (t, mois = "Novembre"):
        jour = 1 + t//(6*24) 
        heure = (t//6) % 24
        minute = 10 * t % 60 
        date = {"Mois":mois,"Jour":jour,"Heure":heure,"Minute":minute}
        return date
    calculDate=staticmethod(calculDate)
if __name__=="__main__":
    print Utilitaire.calculDate(24*6)