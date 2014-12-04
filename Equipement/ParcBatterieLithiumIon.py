# -*-coding:utf-8 -

'''    Fonctionnement :

- une batterie débite un courant donné par activité*PROD_MAX tout comme les autres équipements
NB : si ce courant est négatif c'est que la batterie est en train de stocker
- pour demander à une batterie de produire de l'énergie envoyez lui une consigne positive en %,
si c'est possible la puissance débitée sera de consigne/100 * PROD_MAX
- pour lui demander de stocker vous lui donnez une consigne NEGATIVE (toujours en %)
si c'est possible elle stockera gentiment une puissance de abs(consigne)/100 * PROD_MAX

        Les impossibilités rencontrées par les batteries sont :

- la batterie a plusieurs modes de chargement : rapide, semi-rapide ou lent.
- la surtension (dégradation de la batterie = très cher)
- la sous tension (destruction de la batterie, rendu impossible par le modèle)
- le manque de capacité pour stocker/le manque de stock à déstocker'''

class ParcBatterieLithiumIon:
    
    def __init__(self, nom="un petit parc", nombre = 10, prop = 0.5, activite=0.): #activité en %
        self.nom=nom
        '''nombre de batterie dans le parc'''
        self.nombre = nombre
        '''capacité en kWh'''
        self.capacite = 6.5*self.nombre
        '''énergie stockée dans le parc en kWh'''
        self.reste = self.capacite*prop #pas un pourcentage
        '''production maximale en kW''' #pour la charge rapide
        self.PROD_MAX = 23.*self.nombre
        '''production normale en kW'''
        self.PROD_NOR = 20.*self.nombre
        '''production minimale en kW'''
        self.PROD_MIN = 16.*self.nombre
        self.coefficient_de_charge = 0
        self.choix_possibles_de_charge = [1,1/2,1/4,0]
        '''Les prix sont en €/kWh'''
        self.cout_charge_rapide = 0.9
        self.cout_charge_semi_rapide = 0.5
        self.cout_charge_lente = 0.1
        
        '''EFFACEMENT minimale en kW'''
        self.EFFA_MAX = self.PROD_MAX
        self.effacement=0

        '''Les prix sont en €/kWh'''
        
        '''l'activité est en %'''
        self.activite = activite
        
        '''les compteurs permet d'éviter une trop longue mise en surtension. Au bout
        de 2 pas la batterie se voit obliger d'arrêter le plein régime pour 8 pas de repos'''
        self.compteur_fin = 0
        self.compteur_pause = 3
        
    def etat_suivant(self, consigne=0.): #consigne en pourcentage de PROD_MAX
        '''si la pile a fini une dé/charge elle s'arrête'''
        if self.compteur_fin == 1:
            self.compteur_pause = 0
            self.compteur_fin = 0
            self.activite = 0
            self.coefficient_de_charge = 0
            
            '''si la pile est en mode pause et qu'elle doit le prolonger'''
        elif self.compteur_pause < 2:
            self.compteur_pause += 1
            self.activite = 0
            self.coefficient_de_charge = 0
        
            '''sinon si elle est en état de fonctionnement on éxécute la prévision'''
        else:
            self.activite = self.prevision(consigne)[0]
            if self.activite == 0:
                self.compteur_fin += 1
                self.type_de_charge = 0
            else:
                self.type_de_charge = self.calculType(self.activite)
            self.reste = self.reste + self.activite*self.PROD_MAX/6/100
        
    def prevision(self, consigne=0.): #consigne en pourcentage
        
        '''si la pile entre ou continue son mode de pause'''
        if self.compteur_fin == 1 or self.compteur_pause < 2:
            return (0.,0.)
        
        elif self.contraintes(consigne) == False:
            return (0.,0.)
        
            '''si le fonctionnement va donner lieu à quelque chose'''
        else:
            
            '''cas du stockage'''
            if consigne > 0.:
                '''si la capacité restante est limitée'''
                if self.capacite - self.reste < consigne/100. * self.PROD_MAX/6:
                    prod = (self.capacite-self.reste)*100 / (self.PROD_MAX/6)
                else:
                    prod = consigne
                    
                    '''cas du déstockage'''
            else:
                '''cas où il ne reste pas assez d'énergie dans la pile'''
                if self.reste < - consigne/100. * self.PROD_MAX/6:
                    prod = - self.reste*100 / (self.PROD_MAX/6)
                else:
                    prod = consigne
        
        prix = self.calculPrix(self.calculType(prod))*abs(prod)/100*self.PROD_MAX
        return (prod, prix)
    
    def simulation(self):
        prod_min = self.simulation_destockage()[0]
        prod_max = self.simulation_stockage()[1]
        prix_min = self.simulation_destockage()[2]
        prix_nor = max(self.simulation_stockage()[3],self.simulation_destockage()[3])
        prix_max = self.simulation_stockage()[4]
        return (prod_min,prod_max,prix_min,prix_nor,prix_max)
                
    def simulation_destockage(self):
    
        if self.compteur_fin == 1 or self.compteur_pause < 2 or self.activite > 0:
            '''cas où la batterie commence ou continue une pause due à une surtension'''
            return (0.,0.,0.,0.,0.)
            
        elif self.coefficient_de_charge == 0:
            prix_min = self.calculDecharge(1/4)[2]
            prix_normal = self.calculDecharge(1/2)[3]
            prix_max = self.calculDecharge(1)[4]
            prod_min = self.calculDecharge(1/4)[0]
            prod_max = self.calculDecharge(1)[1]
            return (prod_min, prod_max, prix_min, prix_normal, prix_max)
            
            '''cas où la pile suit un régime constant'''
        else:
                return self.calculDecharge(self.coefficient_de_charge)
    
    def simulation_stockage(self):
    
        if self.compteur_fin == 1 or self.compteur_pause < 2 or self.activite < 0:
            '''cas où la batterie commence ou continue une pause due à une surtension ou à une transition après une décharge'''
            return (0.,0.,0.,0.,0.)
        
            '''cas où la pile sort d'une pause et où elle peut choisir son mode de stockage'''
        elif self.coefficient_de_charge == 0:
            prix_min = self.calculCharge(1/4)[2]
            prix_normal = self.calculCharge(1/2)[3]
            prix_max = self.calculCharge(1)[4]
            prod_min = self.calculCharge(1/4)[0]
            prod_max = self.calculCharge(1)[1]
            return (prod_min, prod_max, prix_min, prix_normal, prix_max)
            
            '''cas où la pile suit un régime constant'''
        else:
                return self.calculCharge(self.coefficient_de_charge)    
        
    
    def contraintes(self,consigne): #consigne en pourcentage
        
        if self.compteur_fin == 1 or self.compteur_pause < 2: #cas de la mise en pause
            if consigne == 0:
                return True
            else:
                return False
        
        if consigne > 0: #cas du stockage
            if consigne >= self.simulation_stockage()[0] and consigne <= self.simulation_stockage()[1]:
                '''on vérifie que la consigne correspond à un système de charge possible'''
                if (consigne >= self.calculCharge(self.choix_possibles_de_charge[2])[0] and consigne <= self.calculCharge(self.choix_possibles_de_charge[2])[1]) or (consigne >= self.calculCharge(self.choix_possibles_de_charge[1])[0] and consigne <= self.calculCharge(self.choix_possibles_de_charge[1])[1]) or (consigne >= self.calculCharge(self.choix_possibles_de_charge[0])[0] and consigne <= self.calculCharge(self.choix_possibles_de_charge[0])[1]):
                    return True
            else:
                return False
            
        elif consigne < 0: #cas du déstockage
            if consigne <= self.simulation_destockage()[0] and consigne >= self.simulation_destockage()[1]:
                return True
            else:
                return False
        else: #non activité
            return True
            
    def calculPrix(self, type_de_charge):
        '''cas surtension'''
        if type_de_charge == self.choix_possibles_de_charge[0]:
            prix = self.cout_charge_rapide
            '''cas semi rapide'''
        elif type_de_charge == self.choix_possibles_de_charge[1]:
            prix = self.cout_charge_semi_rapide
            '''cas charge lente'''
        elif type_de_charge == self.choix_possibles_de_charge[2]:
            prix = self.cout_charge_lente
        else:
            prix = 0
        return prix

    def calculCharge(self, type_de_charge): #calcul les possibilités en fonction du type de charge choisi (rapide, semi-rapide ou lente)
        
        if self.capacite-self.reste >= self.PROD_MAX*type_de_charge/6:
            '''cas idéal où il reste assez pour charger à volonté'''
            prix_min = self.calculPrix(type_de_charge)*self.PROD_MIN*type_de_charge
            prod_min = self.PROD_MIN*type_de_charge/self.PROD_MAX*100
            prix_max = self.calculPrix(type_de_charge)*self.PROD_MAX*type_de_charge
            prod_max = 100*type_de_charge
            prix_normal = self.calculPrix(type_de_charge)*self.activite/100*self.PROD_MAX
            
        else:
            '''cas où il faut prendre en compte le reste'''
            prix_min = self.calculPrix(type_de_charge)*self.PROD_MIN*type_de_charge
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            activite_maximum = (self.capacite-self.reste)/(self.PROD_MAX/6)*100
            prod_max = activite_maximum
            prix_max = self.calculPrix(type_de_charge)*self.PROD_MAX*type_de_charge
            if activite_maximum > abs(self.activite):
                prix_normal = self.calculPrix(type_de_charge)*self.activite/100*self.PROD_MAX
            else:
                prix_normal = prix_max
                
        if prod_min > prod_max:
            prod_max = prod_min
            prix_max = prix_min
            prix_normal = prix_min
        
        return (prod_min, prod_max, prix_min, prix_normal, prix_max)
    
    def calculDecharge(self, type_de_charge): #calcul les possibilités en fonction du type de charge choisi (rapide, semi-rapide ou lente)
        
        if self.reste >= self.PROD_MAX*type_de_charge/6:
            '''cas idéal où il reste assez pour décharger à volonté'''
            prix_min = self.calculPrix(type_de_charge)*self.PROD_MIN*type_de_charge
            prod_min = self.PROD_MIN*type_de_charge/self.PROD_MAX*100
            prix_max = self.calculPrix(type_de_charge)*self.PROD_MAX*type_de_charge
            prod_max = 100*type_de_charge
            prix_normal = self.calculPrix(type_de_charge)*self.activite/100*self.PROD_MAX
            
        else:
            '''cas où il faut prendre en compte le reste'''
            prix_min = self.calculPrix(type_de_charge)*self.PROD_MIN*type_de_charge
            prod_min = self.PROD_MIN/self.PROD_MAX*100
            activite_maximum = self.reste/(self.PROD_MAX/6)*100
            prod_max = activite_maximum
            prix_max = self.calculPrix(type_de_charge)*self.PROD_MAX*type_de_charge
            if activite_maximum > abs(self.activite):
                prix_normal = self.calculPrix(type_de_charge)*self.activite/100*self.PROD_MAX
            else:
                prix_normal = prix_max
                
        if prod_min > prod_max:
            prod_max = prod_min
            prix_max = prix_min
            prix_normal = prix_min
        
        return (-prod_min, -prod_max, prix_min, prix_normal, prix_max)
        
    def calculType(self, activite):
        min = 1000.
        type_de_charge = 0
        puissance = abs(activite)/100*self.PROD_MAX
        for i in self.choix_possibles_de_charge:
            puissance_normale = i*self.PROD_NOR
            tmp = abs(puissance-puissance_normale)
            if tmp < min:
                min = tmp
                type_de_charge = i
        return type_de_charge
        
    #pour les tests
if __name__=='__main__':
    a = ParcBatterieLithiumIon(activite=0, prop=1/5)
    print(a.capacite)
    print(a.reste)
    print(a.contraintes(70.))
    print(a.prevision(70.))
    print(a.simulation_stockage())
    print(a.simulation_destockage())
    print(a.compteur_fin)
    a.etat_suivant(70)
    print(a.type_de_charge)
    print(a.reste)
    print(a.contraintes(-100))
    print(a.prevision(-100))
    print(a.simulation_stockage())
    print(a.simulation_destockage())
    print(a.compteur_fin)
    a.etat_suivant(-100)
    print(a.reste)
    print(a.compteur_fin)
    a.etat_suivant(-100)
    print(a.compteur_fin)
    print(a.compteur_pause)
    a.etat_suivant(-100)
    print(a.compteur_pause)
    a.etat_suivant(-100)
    print(a.activite)
    print(a.compteur_pause)
    print(a.reste)
    print(a.contraintes(-70.))
    print(a.prevision(-70.))
    print(a.simulation_stockage())
    print(a.simulation_destockage())
    print(a.compteur_fin)
