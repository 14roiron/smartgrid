#!/usr/bin/python2.7
# -*-coding:Utf-8-*

import math
from Utilitaire import Global

class ParcEolien:

	"""Constructeur de parc d'éolienne. Par défaut Eolienne 5 kW"""
	def __init__(self,nom="eolienne",n=10,eolienne="eolienne5",meteoVent=Global.meteoTest):
		if eolienne =="eolienne1500":
			dictPV = {0.00:0.00,0.50:0.00,1.00:0.00,1.50:0.00,2.00:0.00,2.50:0.00,3.00:0.00,3.50:20.00,4.00:43.00,4.50:83.00,5.00:131.00,5.50:185.00,6.00:250.00,
6.50:326.00,7.00:416.00,7.50:521.00,8.00:640.00,8.50:780.00,9.00:924.00,9.50:1062.00,10.00:1181.00,10.50:1283.00,11.00:1359.00,11.50:1402.00,
12.00:1436.00,12.50:1463.00,13.00:1481.00,13.50:1488.00,14.00:1494.00,14.50:1500.00,15.00:1500.00,15.50:1500.00,16.00:1500.00,16.50:1500.00,
17.00:1500.00,17.50:1500.00,18.0:1500.00,18.50:1500.00,19.00:1500.00,19.50:1500.00,20.00:1500.00,20.50:1500.00,21.00:1500.00,21.50:1500.00,
22.00:1500.00}
			h = 80
		else:
			dictPV={1:0,2:0,3:14,4:210,5:576,6:1104,7:1783,8:2542,9:3349,10:4077,11:4628,12:4911,13:5066,14:5141,15:5141,16:5159,17:5217,18:5212,19:5242,20:5235}
			h = 20 
		
		self.nbEolienne = n
		self.dictPV = dictPV
		self.listVent = []
		for i in range(len(meteoVent)):
			self.listVent.append(0.13*meteoVent[i]*math.log(h/0.03))


	def prevision(self):

		"""On va chercher la liste des vitesses croissantes"""
		listVitesse = list(self.dictPV.keys())
			
		t=Global.temps
		"""Interpolation linéaire à partir de point de la courbe de puissance"""				
		if self.listVent[t]>listVitesse[len(listVitesse)-1]:	
			return 0
		else:		
			for i in range(len(listVitesse)):
				if i>0:
					if i>=self.listVent[t+1]:
						return self.nbEolienne*(((self.dictPV[i]-self.dictPV[i-1])/(listVitesse[i]-listVitesse[i-1]))*(self.listVent[t+1]-listVitesse[i-1])+self.dictPV[i-1])
						#break#wtf y a déjà un return


	def etatSuivant(self, consigne=100,effacement=0):#pas ce que l'on demande
		self.nbEolienne = int(self.nbEolienne*(consigne/100))
		self.effacement=0
		activite
	
	def contraintes(self,consigne,effacement):#on considère que l'on force le régime nominale, demande à élina
		if consigne<0 or consigne>100:
			return False
		else:
			return True
