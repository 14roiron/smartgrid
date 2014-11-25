class Utilitaire:
    
    def __init__ (self,temps):
        self.date = Utilitaire.calculDate(10*temps)
        self.temps=temps
        
    def calculDate (t, mois = "Avril", jour=1, heure=0, minute=0):
        jour = 1 + t//(60*24) 
        heure = (t//60) % 24
        minute = t % 60 
        date = {"Mois":mois,"Jour":jour,"Heure":heure,"Minute":minute}
        return date
    calculDate=staticmethod(calculDate)
