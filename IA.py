from sklearn import preprocessing,svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
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
#from fuzzywuzzy import fuzz

import nltk
import sklearn

print('The nltk version is {}.'.format(nltk.__version__))
print('The scikit-learn version is {}.'.format(sklearn.__version__))

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
	replace = 0
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
	#nltk.download()

	#X=np.array(X)
	X= list(X)


	np.random.shuffle(X)
	X=StandardScaler().fit_transform(X)
	y=np.array([int(line[13]) for line in X])
	Xcomplement=np.array([line[16:] for line in X])
	X=np.array([line[:13] for line in X])
	np.concatenate((X,Xcomplement),axis=1)

	X_train, X_test, y_train, y_test=train_test_split(X, y, test_size = 0.33, random_state = 42)

	#fim de preparacao
	titles = [
	"K-neighbors",
	"SVC linear",
	"SVC poly",
	#"Gaussian",
	"Decision Tree",
	"Random Forest",
	"MLP",
	"Gaussian with Nayve bayes",
	"Quadratic bayes"
	]
	titlesIter = iter(titles)

	classifiers = [
		KNeighborsClassifier(5),
    	SVC(kernel="linear", C=0.025),
    	SVC(gamma=2, C=1),
    	#GaussianProcessClassifier(1.0 * RBF(1.0)),
    	DecisionTreeClassifier(max_depth=5),
    	RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    	MLPClassifier(alpha=1),
    	GaussianNB(),
    	QuadraticDiscriminantAnalysis()]

	maximum=0
	print('TESTING ACCURACY FROM SOME AI MODELS: ')
	print(' ')
	
	for clf in classifiers:
		clf.fit(X_train,y_train)
		accuracy=clf.score(X_test,y_test)
		print(str(next(titlesIter)),": ",accuracy)
		if replace==1:
			if accuracy>maximum:
				with open('ia1.pickle','wb') as ia:
					pickle.dump(clf,ia)
					maximum=accuracy

	#with open('LinearRegression.pickle','wb') as f:
		#pickle.dump(clf,f)

	#pickle_in = open('LinearRegression.pickle','rb')
	#clf= pickle.load(pickle_in)


	
	# list = new_data_to_be_predicted_somehow()
	#forecast_set =clf.predict()#(list)
	#data_set['Forecast']=forecast_set
