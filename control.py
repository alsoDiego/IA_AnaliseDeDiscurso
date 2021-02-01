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
    #print("text: " + str(text))
    stemmer = SnowballStemmer("portuguese")
    text=text.lower()
    #print("text: " + str(text))
    collectedText =word_tokenize(text)
    #print("finaltext2: " + collectedText)
    tokensMinusPunctuation = [x.rstrip(',\'.&`>0123456789<!?;\")(') for x in collectedText]
    #print("tokensMinusPunctuation:" + str(tokensMinusPunctuation))
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
                dG.node[word]['count'] = 1
            else:
                dG.node[word]['count'] += 1
            if not dG.has_node(nextWord):
                dG.add_node(nextWord)
                dG.node[nextWord]['count']=0
            if not dG.has_edge(word, nextWord):
                dG.add_edge(word, nextWord, weight=1)
            else:
                dG[word][nextWord]['weight']+=1
        except IndexError:
            if not dG.has_node(word):
                dG.add_node(word)
                dG.node[word]['count'] = 1
            else:
                dG.node[word]['count'] += 1
        except:
            raise
    return dG


def searchCycles(dg):
    cycles = list(nx.simple_cycles(dG))
    print("simple search finished. going for big one")
    sizes = [len(g) for g in cycles]
    c1 = len([g for g in sizes if g==1])
    c2 = len([g for g in sizes if g==2])
    c3 = len([g for g in sizes if g==3])
    weakComp = 0
    if len(sizes)>0:
        weakComp = max(sizes)
    try:
        sCycles = list(nx.find_cycle(dG, orientation='original'))
        strongComp =max([len(s) for s in sCycles])
    except:
        strongComp=0
    return c1,c2,c3,weakComp,strongComp


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
    return result

def vectorDistanceNormalized(vectorA, vectorB):
    return spatial.distance.euclidean(vectorA, vectorB)*spatial.distance.cosine(vectorA, vectorB)
#The thing here is that just cossine isn't enough, so the metric we are using is the cossine TIMES the distance between vectors. Hopefully this will be enough.

def vectorCoolCosine(vectorA, vectorB):
    return vectorDistanceNormalized(vectorA, vectorB)

def fixEntryCorpus(row): #Pra ficar mais fácil de tratar, essa função transforma os 8 ultimos caras da entrada num unico vetor8
    result = [row[0]]
    result.append([float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8])])
    return result

def checkCorpus(word):
    for row in emotionCorpus:
        if word == row[0]:
            result = row[1].copy
            return result
        return [0,0,0,0,0,0,0,0]

def calculateMeanLine(lineVector):
    return mn(lineVector)

if __name__ == '__main__':
    path = "control/"
    sentences = []
    output = open('control_data.txt', 'w')
    for filename in os.listdir(path):
        content = open(path+filename,encoding="latin1")
        lines = content.readlines()
        print(filename)
        strLines = str(lines)
        paragraphs = strLines.split("\n")

        #sentences.append(lines)
        content.close()

    #print(sentences[:], sep=' ')
        for sent in paragraphs:
            phrases =sent.split(".")
            filterEmpty = [line for line in phrases if len(line)>0]

            for text in filterEmpty:
                #print("text"+text)
                text2=prepare(text)
                print(filename)
                if len(text2)>0:
                    dG = generateGraph(text2)
                    print(len(dG))
                    repeatedEdges=0
                    for edge in dG.edges():
                        repeatedEdges+=dG[edge[0]][edge[1]]['weight']-1

                    
                    print("search started")
                    c1,c2,c3,maxCycle,maxStrongCycle = searchCycles(dG)
                    print("search finished.")
                    avg = avgDegree(dG)
                    ##daqui comeca a analise de sentimentos
                    with open("NRCEmotion.csv", newline='') as csvfile:
                        emotionCorpus = csv.reader(csvfile, delimiter=';', dialect='excel',)
                        emotionCorpus = map(fixEntryCorpus, emotionCorpus)
                        #corpus = open("corpus.txt")
                        tokenList = phrases[:]
                        line = []
                        sentences = []
                        counter = 0
                        sentenceVector = [0,0,0,0,0,0,0,0]
                        emotionalVariance = []
                        for sentence in tokenList:
                            for word in sentence:
                                line.append(checkCorpus(word))
                            for vector in line:
                                sentenceVector = vectorSum(vector, sentenceVector)
                            sentences.append(sentenceVector)
                            line = []
                            sentenceVector = [0,0,0,0,0,0,0,0]
                        for i in range(0,len(sentences)):
                            try:
                                emotionalVariance.append(vectorCoolCosine(sentences[i],sentences[i+1]))
                                i += 1
                            except IndexError:
                                break
                        ##aqui termina
                        adding = reduce ((lambda x,y: x+y),emotionalVariance)
                        adding = adding/len(emotionalVariance)
                        components =[repeatedEdges,c1,c2,c3,maxCycle,maxStrongCycle,avg]
                        components.append(adding)
                        components.append(1)
                        components.append(0)
                        components.append(0)
                        if (repeatedEdges+c1+c2+c3+maxCycle+maxStrongCycle)>0:
                            answer= "["
                            for i in components:
                                answer = answer + str(i) + ","
                            output.write(answer[:-1]+"]\n")
                            print(answer)
    output.close()
