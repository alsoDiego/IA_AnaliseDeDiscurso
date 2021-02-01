import numpy as np
from functools import reduce
import math

if __name__=="__main__":

	file=open("patient_data.txt",'r')
	data_set = file.read()
	data_set=data_set.splitlines()
	#re.split("[.*?]",data_set)
	esqui = []
	control = []
	for line in data_set:
		line = line.replace("[","")
		line = line.replace("]","")
		line = line.replace("nan","0")
		line=line.split(",")
		#print(line)
		if int(line[13])==1:
			control.append(line)
		else:
			esqui.append(line)
	medias=np.array([0.0]*13)
	medianas=np.array([0.0]*13)
	variancia=np.array([0.0]*13)
	maximo=np.array([0.0]*13)
	minimo=np.array([0.0]*13)
	for i in range(13):
		if i!=9:
			column = np.array([float(line[i]) for line in esqui])
			length = len(column)
			mean = np.mean(column)
			medias[i]=mean
			medianas[i]=np.median(column)
			variancia[i]=math.sqrt(np.var(column))
			maximo[i]=max(column)
			minimo[i]=min(column)

	Cmedias=np.array([0.0]*13) #A letra C no comeco se refere ao grupo de controle
	Cmedianas=np.array([0.0]*13)
	Cvariancia=np.array([0.0]*13)
	Cmaximo=np.array([0.0]*13)
	Cminimo=np.array([0.0]*13)
	for i in range(13):
		if i!=9:
			column = np.array([float(line[i]) for line in control])
			length = len(column)
			mean = np.mean(column)
			Cmedias[i]=mean
			Cmedianas[i]=np.median(column)
			Cvariancia[i]=math.sqrt(np.var(column))
			Cmaximo[i]=max(column)
			Cminimo[i]=min(column)
	medias=np.concatenate((medias,Cmedias),axis=0)
	variancia=np.concatenate((variancia,Cvariancia),axis=0)
	#medias=[row / np.linalg.norm(medias) for row in medias]
	#Cmedias=[row / np.linalg.norm(Cmedias) for row in Cmedias]
	#variancia=[row / np.linalg.norm(variancia) for row in variancia]
	#Cvariancia=[row / np.linalg.norm(Cvariancia) for row in Cvariancia]
	#maximo=[row / np.linalg.norm(maximo) for row in maximo]
	#minimo=[row / np.linalg.norm(minimo) for row in minimo]
	#Cmaximo=[row / np.linalg.norm(Cmaximo) for row in Cmaximo]
	#Cminimo=[row / np.linalg.norm(Cminimo) for row in Cminimo]

	for i in range(13):
		column_esqui = np.array([float(line[i]) for line in esqui])
		column_control = np.array([float(line[i]) for line in control])
		line = [np.mean(column_esqui),np.mean(column_control),math.sqrt(np.var(column_esqui)),math.sqrt(np.var(column_control))]
		#line = [value / np.linalg.norm(line) for value in line]
		print(i,":",line)
	print(len(data_set))
	#print("media",medias)
	#print("mediana",medianas)
	#print("variancia",variancia)
	#print("maximo",maximo)
	#print("minimo",minimo)
	#print("media",Cmedias)
	#print("mediana",Cmedianas)
	#print("variancia",Cvariancia)
	#print("maximo",Cmaximo)
	#print("minimo",Cminimo)

