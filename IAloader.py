import pickle
import graph as gr
pickle_in = open('ia1.pickle','rb')
clf= pickle.load(pickle_in)

data= input()
prediction = clf.predict(gr.metric(data))
if  prediction >=0.5:
	print("is probably not sick")
else:
	print("is probably sick")