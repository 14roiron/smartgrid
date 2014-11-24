# -*-coding:Utf-8 -*
class Equipement:
	def __init__(self,prod,effa):
		"""int production maximale, effacement maximal en %"""
		self.PROD_MAX=prod
		self.activite=0
		self.EFFA_MAX=effa
		self.effacement=0
	
	def prevision(self,consigne):
		""" renvoie le tuple (production prévue, coût prévu) pour la consigne donnée"""
		return (0,0)
	
	def simulation(self):
		"""renvoie le tuple (prod minimale, prod maximale, coût minimal, coût stable, coût maximal)
		pour l'étape suivante"""
		return (0,0,0,0,0)
	
	def etatSuivant(self,consigne):
		"""modifie les attributs à partir de la consigne"""
		pass
	
	def contraintes(consigne):
		"""renvoie un booléen ; dit si la consigne peut être exécutée ou non en fonction des contraintes
		spécifiques à la classe considérée. Ex : une centrale thermique ne peut pas s'arrêter avant 3h de
		fonctionnement, donc on renvoie false si la consigne est de s'arrêter alors que le temps de
		fonctionnement est <3h."""
		pass
