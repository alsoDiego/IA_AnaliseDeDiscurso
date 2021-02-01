from sklearn import preprocessing,cross_validation,svm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import sklearn
import numpy as np
import math
import pandas as pd
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from fuzzywuzzy import fuzz

#import regex as re
def extract_features(list):
	for x in list:		
		x.append(fuzz.QRatio(x[:13],x[13]))
		x.append(fuzz.partial_ratio(x[:13],x[13]))
		x.append(fuzz.partial_token_set_ratio(x[:13],x[13]))
		x.append(fuzz.partial_token_sort_ratio(x[:13],x[13]))
		x.append(fuzz.token_set_ratio(x[:13],x[13]))
		x.append(fuzz.token_sort_ratio(x[:13],x[13]))
	return list
if __name__=="__main__":

	file = open("patient_data.txt",encoding="latin1") #o endereco pode mudar
	data_set = file.read()
	data_set=data_set.splitlines()
	#re.split("[.*?]",data_set)
	X = []
	for line in data_set:
		line = line.replace("[","")
		line = line.replace("]","")
		line = line.replace("nan","0")
		line=line.split(",")
		X.append(line)
	
	#X['repeatedEdges'] = data_set[0]
	#X['C1']=data_set[1]
	#X['C2']=data_set[2]
	#X['C3']=data_set[3]
	#X['weakComp']=data_set[4]
	#X['strongComp']=data_set[5]
	#X['avgDegree']=data_set[6]
	#X['diameter']=data_set[7]
	#X['shortest']=data_set[8]
	#X['size']=data_set[9]
	#X['edges']=data_set[10]
	#X['nodes']=data_set[11]
	#X['emtVariance']=data_set[12]
	#X['healthy']=data_set[13] #normal
	#X['eqf']=data_set[14] #esquizofrenia
	#X['aut']=data_set[15] #autismo
	
	#X = extract_features(X)
	#print (X)

	X=np.array(X)
	np.random.shuffle(X)
	print (str(type(X)))
	X=StandardScaler().fit_transform(X)
	y=np.array([int(line[13]) for line in X])
	Xcomplement=np.array([line[16:] for line in X])
	X=np.array([line[:13] for line in X])
	np.concatenate((X,Xcomplement),axis=1)
	X_train,X_test,y_train,y_test = cross_validation.train_test_split(X,y, test_size=0.2)

	clf=DecisionTreeClassifier(max_depth=5)
	#svmy=np.array([line[0] for line in y])
	clf.fit(X_train,y_train)
	accuracy=clf.score(X_test,y_test)
	features = clf.feature_importances_
	for f in features:
		print(f)

	#with open('LinearRegression.pickle','wb') as f:
		#pickle.dump(clf,f)

	#pickle_in = open('LinearRegression.pickle','rb')
	#clf= pickle.load(pickle_in)


	
	# list = new_data_to_be_predicted_somehow()
	#forecast_set =clf.predict()#(list)
	#data_set['Forecast']=forecast_set
