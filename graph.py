from nltk.corpus import reuters
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from scipy import spatial
from nltk import word_tokenize, sent_tokenize
from numpy import linalg as la
from numpy import mean as mn
from scipy import spatial
from copy import copy,deepcopy
import networkx as nx
import os
import csv
from functools import reduce
#from stackoverflow import mycode

def prepare (text):
    stemmer = SnowballStemmer("portuguese")
    text=text.lower()
    collectedText =word_tokenize(text)
    tokensMinusPunctuation = [x.rstrip(',\'.&`>0123456789<!?;\")(') for x in collectedText]
    tokensMinusStopwords = [word for word in tokensMinusPunctuation if word not in stopwords.words('portuguese')]
    tokensMinusEmpty = [word for word in tokensMinusStopwords if word!= ""]
    finalText = [stemmer.stem(word) for word in tokensMinusEmpty]
    return finalText

def generateGraph(text):
    dG = nx.DiGraph()
    for i, word in enumerate(text):
        try:
            nextWord = text[i+1]
            if not dG.has_node(word):
                dG.add_node(word)
                dG.nodes[word]['count'] = 1
            else:
                dG.nodes[word]['count'] += 1
            if not dG.has_node(nextWord):
                dG.add_node(nextWord)
                dG.nodes[nextWord]['count']=0
            if not dG.has_edge(word, nextWord):
                dG.add_edge(word, nextWord, weight=1)
            else:
                dG[word][nextWord]['weight']+=1
        except IndexError:
            if not dG.has_node(word):
                dG.add_node(word)
                dG.nodes[word]['count'] = 1
            else:
                dG.nodes[word]['count'] += 1
        except:
            raise
    return dG


def searchCycles(dG):
    cycles = list(nx.simple_cycles(dG))
    #print("simple search finished. going for big one")
    sizes = [len(g) for g in cycles]
    size2=len(dG.edges)
    yield len([g for g in sizes if g==1])
    yield len([g for g in sizes if g==2])
    yield len([g for g in sizes if g==3])
    weakComp = 0
    if len(sizes)>0:
        weakComp = max(sizes)
    yield weakComp
    try:
        sCycles = list(nx.find_cycle(dG, orientation='original'))
        yield max([len(s) for s in sCycles])
    except:
        yield 0
    try:
        yield nx.diameter(dG)
    except:
        yield len(dG)

    yield nx.average_shortest_path_length(dG)
    yield len(dG.edges)
    yield len(dG)

def avgDegree(dG):
    return float(len(dG.edges))/float(len(dG))

def prepareTwo (text):
    text=[f.lower() for f in text]
    final =[word_tokenize(word) for word in text]
    finalText = ""
    for a in final:
        finalText = finalText + str(a) + " "

    return finalText

def normalize(Originalvector):
    vector = Originalvector
    norm = la.norm(vector)
    for i in range(len(vector)):
        if norm != 0:
            vector[i] = vector[i] / norm
        else: return vector
        return vector

def vectorSum(vectorA, vectorB):
    if (type(vectorA) is list) & (type(vectorB) is list):
        result = [vectorA[0]+vectorB[0],vectorA[1]+vectorB[1],vectorA[2]+vectorB[2],vectorA[3]+vectorB[3],
              vectorA[4]+vectorB[4],vectorA[5]+vectorB[5],vectorA[6]+vectorB[6],vectorA[7]+vectorB[7]]
    elif type(vectorA) is list:
        result = vectorA
    elif type(vectorB) is list:
        result = vectorB
    else:
        result = [0]*8
    if None in result:
        return [0]*8
    return result

def vectorDistanceNormalized(vectorA, vectorB):
    return spatial.distance.euclidean(vectorA, vectorB)#*spatial.distance.cosine(vectorA, vectorB)
    
#The thing here is that just cossine isn't enough, so the metric we are using is the cossine TIMES the distance between vectors. Hopefully this will be enough.

def vectorCoolCosine(vectorA, vectorB):
    return vectorDistanceNormalized(vectorA, vectorB)

def fixEntryCorpus(row):
    result = [row[0]]
    result.extend([float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8])])
    return result

def checkCorpus(sentence,emotionCorpus):
    phrase = ''.join(sentence)
    phrase = phrase.lower()
    result=[0]*8
    for row in emotionCorpus:
        if str(row[0]) in phrase:
            #print("achou")
            for i in range(8):
                result[i]=result[i]+row[i+1]
    return result

def calculateMeanLine(lineVector):
    return mn(lineVector)

def addition(vecA,vecB):
    print(str(vecA),str(vecB))
    if len(vecA)>len(vecB):
        answer=vecA.copy()
        for i in range(len(vecB)):
            answer[i] = answer[i]+vecB[i]
    else:
        answer=vecB.copy()
        for i in range(len(vecA)):
            answer[i] = answer[i]+vecA[i]
    return answer
def metric(paragraphs):
    vectorMean=[0]*8
    index =0
    for sent in paragraphs:
        phrases =sent.split(".")
        filterEmpty = [line for line in phrases if len(line)>0]
        for text in filterEmpty:
            #print("text"+text)
            text2=prepare(text)
            #print(filename)
            if len(text2)>0:
                dG = generateGraph(text2)
                #print(len(dG))
                repeatedEdges=0
                for edge in dG.edges():
                    repeatedEdges+=dG[edge[0]][edge[1]]['weight']-1

                    
                #print("search started")
                c1,c2,c3,maxCycle,maxStrongCycle,diameter,shortest,edges,nodes = searchCycles(dG)
                #print("search finished.")
                avg = avgDegree(dG)
                ##daqui comeca a analise de sentimentos
                with open("NRCEmotion.csv", newline='') as csvfile:
                    emotionCorpus = csv.reader(csvfile, delimiter=';', dialect='excel',)
                    emotionCorpus = map(fixEntryCorpus, emotionCorpus)
                    #corpus = open("corpus.txt")
                    #tokenList = phrases
                    #print(str(phrases)," ",str(paragraphs))
                    line = [0]*8
                    sentences = []
                    counter = 0
                    #sentenceVector = [0,0,0,0,0,0,0,0]
                    emotionalVariance = []
                    for sentence in phrases:
                        sentences.append(checkCorpus(sentence,emotionCorpus))
                    for i in range(len(sentences)-1):
                        try:
                            emotionalVariance.append(vectorCoolCosine(sentences[i],sentences[i+1]))
                        except IndexError:
                            break
                    #print("sentences: "+str(sentences))
                    #print("emotionalVariance"+str(emotionalVariance))
                    ##aqui termina
                    if len(emotionalVariance)>0:
                        adding = reduce ((lambda x,y: x+y),emotionalVariance)
                        adding = adding/len(emotionalVariance)
                    else:
                        adding=0
                        
                    components =[repeatedEdges,c1,c2,c3,maxCycle,maxStrongCycle,avg,diameter,shortest,len(text),edges,nodes]
                    components.append(adding)
                    components.append(control)
                    components.append(esqui)
                    components.append(autism)
                    if len(text)>4:
                        vectorMean=vectorSum(components,vectorMean)
                        index=index+1
    vectorMean=[i/index for i in vectorMean]
    return vectorMean

def getcsv(path,control,esqui,autism):
    sentences = []
    for filename in os.listdir(path):
        content = open(path+filename,encoding="latin1")
        lines = content.read()

        print(filename)
        strLines = str(lines)
        paragraphs=lines.splitlines()

        #sentences.append(lines)
        content.close()

        for sent in paragraphs:
            phrases =sent.split(".")
            filterEmpty = [line for line in phrases if len(line)>0]

            for text in filterEmpty:
                #print("text"+text)
                text2=prepare(text)
                #print(filename)
                if len(text2)>0:
                    dG = generateGraph(text2)
                    #print(len(dG))
                    repeatedEdges=0
                    for edge in dG.edges():
                        repeatedEdges+=dG[edge[0]][edge[1]]['weight']-1

                    
                    #print("search started")
                    c1,c2,c3,maxCycle,maxStrongCycle,diameter,shortest,edges,nodes = searchCycles(dG)
                    #print("search finished.")
                    avg = avgDegree(dG)
                    ##daqui comeca a analise de sentimentos
                    with open("NRCEmotion.csv", newline='') as csvfile:
                        emotionCorpus = csv.reader(csvfile, delimiter=';', dialect='excel',)
                        emotionCorpus = map(fixEntryCorpus, emotionCorpus)
                        #corpus = open("corpus.txt")
                        #tokenList = phrases
                        #print(str(phrases)," ",str(paragraphs))
                        line = [0]*8
                        sentences = []
                        counter = 0
                        #sentenceVector = [0,0,0,0,0,0,0,0]
                        emotionalVariance = []
                        for sentence in phrases:
                            sentences.append(checkCorpus(sentence,emotionCorpus))
                        for i in range(len(sentences)-1):
                            try:
                                emotionalVariance.append(vectorCoolCosine(sentences[i],sentences[i+1]))
                            except IndexError:
                                break
                        #print("sentences: "+str(sentences))
                        #print("emotionalVariance"+str(emotionalVariance))
                        ##aqui termina
                        if len(emotionalVariance)>0:
                            adding = reduce ((lambda x,y: x+y),emotionalVariance)
                            adding = adding/len(emotionalVariance)
                        else:
                            adding=0
                        
                        components =[repeatedEdges,c1,c2,c3,maxCycle,maxStrongCycle,avg,diameter,shortest,len(text),edges,nodes]
                        components.append(adding)
                        components.append(control)
                        components.append(esqui)
                        components.append(autism)
                        yield components
                            
  

