#!/usr/bin/python2.7
# -*-coding:Utf-8-*

from math import *
from Utilitaire import Global
from Equipement import Equipement
from test.regrtest import printlist

class ParcEolien(Equipement):


	nbParc=0

	"""Constructeur de parc d'éolienne. Par défaut Eolienne 5 kW"""	
	def __init__(self,n=10,eolienne="eolienne5",meteoVent=Global.meteo1,nom="Parc d'éolien n°0"):
		
		ParcEolien.nbParc += 1

		if eolienne =="eolienne1500":
			dictPV = {0:0,0.50:0,1:0,1.50:0,2:0,2.50:0,3:0,3.50:20,4:43,4.50:83,5:131,5.50:185,6:250,
6.50:326,7:416,7.50:521,8:640,8.50:780,9:924,9.50:1062,10:1181,10.50:1283,11:1359,11.50:1402,
12:1436,12.50:1463,13:1481,13.50:1488,14:1494,14.50:1500,15:1500,15.50:1500,16:1500,16.50:1500,
17:1500,17.50:1500,18:1500,18.50:1500,19:1500,19.50:1500,20:1500,20.50:1500,21:1500,21.50:1500,
22:1500}
			h = 80
			self.PROD_MAX = 5500 * n
			self.cout = 70 #"""cout en euro par MWh"""
		else:
			dictPV={0:0,1:0,2:0,3:14,4:210,5:576,6:1104,7:1783,8:2542,9:3349,10:4077,11:4628,12:4911,13:5066,14:5141,15:5141,16:5159,17:5217,18:5212,19:5242,20:5235}
			h = 20 
			self.PROD_MAX = 120 * n
			self.cout = 65 #"""cout en euro par MWh"""
			
		self.nbEolienne = n
		self.dictPV = dictPV
		self.listVent = []
		for i in range(len(meteoVent)):
			self.listVent.append(0.13*meteoVent[i]["windSpeed"]*log(h/(exp(log(10)-(1/0.13)))))
		
		self.EFFA_MAX = 0
		self.effacement = 0
		self.nom = nom
		self.activite = 0
		self.previsionb=[0] # à quoi sert cette varriable?


	def prevision(self):

		"""On va chercher la liste des vitesses croissantes"""
		listVitesse = list(self.dictPV.keys())
			
				
		"""Interpolation linéaire à partir de point de la courbe de puissance"""				
		if self.listVent[Global.temps]>listVitesse[len(listVitesse)-1]:	
			return (0,0)
		else:		
			for i in range(1,len(listVitesse)):
				if i>=self.listVent[Global.temps+1]:
					P = self.nbEolienne*((((self.dictPV[i]-self.dictPV[i-1]))/(listVitesse[i]-listVitesse[i-1]))*(self.listVent[Global.temps+1]-listVitesse[i-1])+self.dictPV[i-1])
					self.previsionb[0] = (P/self.PROD_MAX)*100						
					return (P,(P/6)*self.cout) 


		
	def simulation(self): #revoir le prototype de la fonction!
		return (self.prevision()[0],self.prevision()[0],10,20,30)#0,self.prevision[1],(self.PROD_MAX/6)*100)

	def etatSuivant(self, consigne=100, effacement=0):
		if (consigne/100)*self.PROD_MAX<self.prevision()[0]:		
			self.nbEolienne = int(self.nbEolienne*(self.prevision()[0]/self.PROD_MAX))
		self.activite=self.prevision()[0]#faux mais non
	
if __name__=="__main__":
	a=ParcEolien()
	a.etatSuivant(100, 100)
	Global.temps=39
	print a.previsionb[0]
	a.etatSuivant(100, 100)
	print a.activite
	print a.nbEolienne
