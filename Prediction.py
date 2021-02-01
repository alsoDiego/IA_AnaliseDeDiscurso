import IAloader as ia 
#import IAloader2 as ia2 
#import IAloader3 as ia3

data= input()
predictions =[]
predictions.append(ia.predict(data))
#predictions.append(ia2.predict(data))
#predictions.append(ia3.predict(data))

print("chance de ser saudavel: ",predictions[0])
print("chance de ter esquizofrenia: ", predictions[1])
print("chance de ter autismo:",predictions[2])

state = max(predictions)
if state == predictions[0]:
	print("a pessoa esta saudavel")
elif state == predictions[1]:
	print("a pessoa tem esquizofrenia")
elif state == predictions[2]:
	print("a pesssoa tem autismo")