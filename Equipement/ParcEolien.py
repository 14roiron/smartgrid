#!/usr/bin/python2.7
# -*-coding:Utf-8-*

from math import *
from Utilitaire import Global
from Equipement import Equipement
from test.regrtest import printlist

class ParcEolien(Equipement):


	nbParc=0

	"""Constructeur de parc d'éolienne. Par défaut Eolienne 5 kW"""	
	def __init__(self,n=10,eolienne="eolienne5",meteoVent=Global.meteo1):
		
		ParcEolien.nbParc += 1

		if eolienne =="eolienne1500":
			dictPV = {0.00:0.00,0.50:0.00,1.00:0.00,1.50:0.00,2.00:0.00,2.50:0.00,3.00:0.00,3.50:20.00,4.00:43.00,4.50:83.00,5.00:131.00,5.50:185.00,6.00:250.00,
6.50:326.00,7.00:416.00,7.50:521.00,8.00:640.00,8.50:780.00,9.00:924.00,9.50:1062.00,10.00:1181.00,10.50:1283.00,11.00:1359.00,11.50:1402.00,
12.00:1436.00,12.50:1463.00,13.00:1481.00,13.50:1488.00,14.00:1494.00,14.50:1500.00,15.00:1500.00,15.50:1500.00,16.00:1500.00,16.50:1500.00,
17.00:1500.00,17.50:1500.00,18.00:1500.00,18.50:1500.00,19.00:1500.00,19.50:1500.00,20.00:1500.00,20.50:1500.00,21.00:1500.00,21.50:1500.00,
22.00:1500.00}
			h = 80
			PROD_MAX = 1500 * n
			self.cout = 70 """cout en euro par MWh"""
		else:
			dictPV={1:0,2:0,3:14,4:210,5:576,6:1104,7:1783,8:2542,9:3349,10:4077,11:4628,12:4911,13:5066,14:5141,15:5141,16:5159,17:5217,18:5212,19:5242,20:5235}
			h = 20 
			PROD_MAX = 5200 * n
			self.cout = 65 """cout en euro par MWh"""
			
		self.nbEolienne = n
		self.dictPV = dictPV
		listVent = []
		for i in range(len(meteoVent)):
			listVent.append(meteoVent[i]["windSpeed"]*(h/10)**(0.143))
		self.listVent = listVent
		self.EFFA_MAX = 0
		self.effacement = 0
		self.Nom = "Parc d'éolien n°" + str(ParcEolien.nbParc)
		self.activite = 0


	def prevision(self):

		"""On va chercher la liste des vitesses croissantes"""
		listVitesse = list(self.dictPV.keys())
			
				
		"""Interpolation linéaire à partir de point de la courbe de puissance"""				
		if self.listVent[t]>listVitesse[len(listVitesse)-1]:	
			return (0,0)
		else:		
			for i in range(1,len(listVitesse)):
					if listVistesse[i]>=self.listVent[Global.temps+1]:
						P = self.nbEolienne*(((self.dictPV[listVitesse[i]]-self.dictPV[listVitesse[i-1]])/(listVitesse[i]-listVitesse[i-1]))*(self.listVent[Global.temps+1]-listVitesse[i-1])+self.dictPV[listVitesse[i-1]])						
						return (P,(P/6)*self.cout) 


		
	def simulation()
		return(0,self.prevision()[0],0,self.prevision()[1],(PROD_MAX/6)*100)

	def etatSuivant(self, consigne=100, effacement=0)
		if (consigne/100)*PROD_MAX<self.prevision()[0]:		
			self.nbEolienne = int(self.nbEolienne*(self.prevision()[0]/PROD_MAX))
		self.activite = consigne

	def contrainte(self)
		return True

	
if __name__=="__main__":
	a=ParcEolien()
	a.etatSuivant(100)
	Global.temps=39
	print a.activite
	print a.nbEolienne
