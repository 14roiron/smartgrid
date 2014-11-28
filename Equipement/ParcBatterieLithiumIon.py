# -*-coding:utf-8 -

'''    Fonctionnement :

- une batterie débite un courant donné par activité*PROD_MAX tout comme les autres équipements
NB : si ce courant est négatif c'est que la batterie est en train de stocker
- pour demander à une batterie de produire de l'énergie envoyez lui une consigne positive en %,
si c'est possible la puissance débitée sera de consigne/100 * PROD_MAX
- pour lui demander de stocker vous lui donnez une consigne NEGATIVE (toujours en %)
si c'est possible elle stockera gentiment une puissance de abs(consigne)/100 * PROD_MAX

        Les impossibilités rencontrées par les batteries sont :

- la surtension (dégradation de la batterie = très cher)
- la sous tension extensive (destruction de la batterie, rendu impossible par le modèle)
- le manque de capacité pour stocker/le manque de stock à déstocker'''

#chocolatine

class ParcBatterieLithiumIon:
    
    def __init__(self, nom="un petit parc", nombre = 10, prop = 0.5, activite=0.): #activité en %
        self.nom=nom
        '''nombre de batterie dans le parc'''
        self.nombre = nombre
        '''capacité en kWh'''
        self.capacite = 6.5*self.nombre
        '''énergie stockée dans le parc en kWh'''
        self.reste = self.capacite*prop #pas un pourcentage
        '''production maximale en kW'''
        self.PROD_MAX = 23.*self.nombre
        self.COUT_MAX = 0.7
        '''production normale en kW'''
        self.PROD_NOR = 20.*self.nombre
        self.COUT_NOR = 0.1
        '''production minimale en kW'''
        self.PROD_MIN = 17.*self.nombre
        self.COUT_MIN = 0.1
        '''Les prix sont en €/kWh'''
        
        '''l'activité est en %'''
        self.activite = activite
        '''les compteurs permet d'éviter une trop longue mise en surtension. Au bout
        de 2 pas la batterie se voit obliger d'arrêter le plein régime pour 8 pas de repos'''
        self.compteur_surtension = 0
        self.compteur_pause = 8
        
    def etat_suivant(self, consigne=0): #consigne en pourcentage de PROD_MAX
        '''si la pile est depuis trop longtemps en surtension elle s'arrête'''
        if self.compteur_surtension == 2:
            self.compteur_pause = 0
            self.compteur_surtension = 0
            self.activite = 0
            
            '''si la pile est en mode pause et qu'elle doit le prolonger'''
        elif self.compteur_pause < 8:
            self.compteur_pause += 1
            self.activite = 0
        
            '''sinon si elle est en état de fonctionnement on éxécute la prévision'''
        else:
            self.activite = self.prevision()[0]
            self.reste += self.activite/6
        
    def prevision(self,consigne=0.): #consigne en pourcentage
        
        '''si la pile entre ou continue son mode de pause'''
        if self.compteur_surtension == 2 or self.compteur_pause < 8:
            return (0,0)
        
            '''si le fonctionnement va donner lieu à quelque chose'''
        else:
            
            '''cas du stockage'''
            if consigne > 0:
                '''si la capacité restante est limitée'''
                if self.capacite-self.reste < consigne/100. * self.PROD_MAX/6:
                    prod = (self.capacite-self.reste)*100 / (self.PROD_MAX/6)
                else:
                    prod = consigne
                    
                    '''cas du déstockage'''
            else:
                '''cas où il ne reste pas assez d'énergie dans la pile'''
                if self.reste < -consigne/100. * self.PROD_MAX/6:
                    prod = self.reste*100 / (self.PROD_MAX/6)
                else:
                    prod = consigne
            prod = - prod #on déstocke donc la production est négative
        
        prix = self.calculPrix(prod)
        return (prod, prix)
    
    def simulation_destockage(self):
    
        if self.compteur_surtension == 2 or self.compteur_pause < 8:
            '''cas où la batterie commence ou continue une pause due à une surtension'''
            prod_min=0
            prod_max=0
            prix_min=0
            prix_max=0
            prix_normal=0
            
        elif self.reste>=self.PROD_MAX/6:
            '''cas idéal où il reste assez pour décharger à volonté'''
            prix_min = self.COUT_MIN*self.PROD_MIN/6
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            prix_max = self.COUT_MAX*self.PROD_MAX/6
            prod_max = 100
            prix_normal = self.calculPrix(self.activite)

        else:
            '''cas où il faut prendre en compte le reste'''
            prix_min = self.COUT_MIN*self.PROD_MIN/6
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            activite = abs(self.activite)
            activite_maximum = self.reste/(self.PROD_MAX/6)*100
            prod_max = activite_maximum
            prix_max = self.calculPrix(activite_maximum)
            if activite_maximum > activite:
                prix_normal = self.calculPrix(activite)
            else:
                prix_normal = prix_max
        return (-prod_min,-prod_max, prix_min, prix_normal, prix_max)
    
    def simulation_stockage(self):
    
        if self.compteur_surtension == 2 or self.compteur_pause < 8:
            '''cas où la batterie commence ou continue une pause due à une surtension'''
            prod_min=0
            prod_max=0
            prix_min=0
            prix_max=0
            prix_normal=0
            
        elif self.capacite-self.reste>=self.PROD_MAX/6:
            '''cas idéal où il reste assez pour charger à volonté'''
            prix_min = self.COUT_MIN*self.PROD_MIN/6
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            prix_max = self.COUT_MAX*self.PROD_MAX/6
            prod_max = 100
            prix_normal = self.calculPrix(self.activite)
            
        else:
            '''cas où il faut prendre en compte le reste'''
            prix_min = self.COUT_MIN*self.PROD_MIN/6
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            activite_maximum = (self.capacite-self.reste)/(self.PROD_MAX/6)*100
            prod_max = activite_maximum
            prix_max = self.calculPrix(activite_maximum)
            if activite_maximum > abs(self.activite):
                prix_normal = self.calculPrix(self.activite)
            else:
                prix_normal = prix_max
        return (prod_min, prod_max, prix_min, prix_normal, prix_max)    
    
    def contraintes(self,consigne): #consigne en pourcentage
        '''si la puissance demandée (à produire comme à stocker) est 
        inférieure à la minimale que peut fournir le parc ça ne marche pas'''
        if abs(consigne)/100 < self.PROD_MIN/self.PROD_MAX:
            return False
        else:
            '''s'il n'y a plus assez d'énergie dans le parc on ne peut pas produire '''
            if consigne > 0 and consigne*self.PROD_MAX/6 > self.reste:
                return False
            '''s'il ne reste pas assez de place dans les batteries pour stocker ça ne fonctionnera pas non plus'''
            if consigne < 0 and abs(consigne)*self.PROD_MAX/6 > self.capacite - self.reste:
                return False
            else:
                return True
            
    def calculPrix(self, activite):
        if abs(activite)/100*self.PROD_MAX > self.PROD_NOR:
            prix = 10000*(1-100/activite)/1700 + self.COUT_NOR
            '''cas normal'''
        else:
            prix = self.COUT_NOR*activite/100*self.PROD_MAX/6
        return prix

'''vous êtes arrivé au bout félicitations !'''

    #pour les tests
if __name__=='__main__':
    a = ParcBatterieLithiumIon(activite=100, prop=1/5)
    print(a.simulation_stockage())
    print(a.simulation_destockage())
    a.etat_suivant(6)
    print(a.simulation_stockage())
    