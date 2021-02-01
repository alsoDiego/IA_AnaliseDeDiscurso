import csv

from nltk import word_tokenize, sent_tokenize
from numpy import linalg as la
from numpy import mean as mn
from scipy import spatial
from copy import copy,deepcopy

def prepare (text):
    text=text.lower()
    finalText = (word_tokenize(t) for t in sent_tokenize(text))
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
    result = [vectorA[0]+vectorB[0],vectorA[1]+vectorB[1],vectorA[2]+vectorB[2],vectorA[3]+vectorB[3],
              vectorA[4]+vectorB[4],vectorA[5]+vectorB[5],vectorA[6]+vectorB[6],vectorA[7]+vectorB[7]]
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

def fixEntryCorpus2(corpus):
    newCorpus = []
    for row in corpus:
        rowIterator = []
        vectorIterator = []
        rowIterator.append(row[0])
        vectorIterator.append(int(row[1]))
        vectorIterator.append(int(row[2]))
        vectorIterator.append(int(row[3]))
        vectorIterator.append(int(row[4]))
        vectorIterator.append(int(row[5]))
        vectorIterator.append(int(row[6]))
        vectorIterator.append(int(row[7]))
        vectorIterator.append(int(row[8]))
        rowIterator.append(vectorIterator)
        newCorpus.append(deepcopy(rowIterator))
    return newCorpus

def checkCorpus2(word):
    for iterator in range(0, len(emotionCorpus)):
        if word == emotionCorpus[iterator][0]:
            return emotionCorpus[iterator][1]
    return [1,1,1,1,1,1,1,1]

def checkCorpus(word):
    for row in emotionCorpus:
        if word == row[0]:
            return row[1]
    return [1, 1, 1, 1, 1, 1, 1, 1]

def calculateMeanLine(lineVector):
    return mn(lineVector)


#file = open("NRCEmotion.csv", "r")
with open("NRCEmotion.csv", newline='') as csvfile:
    emotionCorpus = csv.reader(csvfile, delimiter=';', dialect='excel',)
    emotionCorpus = fixEntryCorpus2(emotionCorpus)
#    emotionCorpus1 = map(fixEntryCorpus, emotionCorpus)
    corpus = open("corpus.txt")
    tokenList = prepare(corpus.read())
    line = []
    sentences = []
    counter = 0
    emotionalVariance = []
    for sentence in tokenList:
        for word in sentence:
            result = checkCorpus(word)
            line.append(result)
        sentenceVector = [0, 0, 0, 0, 0, 0, 0, 0]
        for vector in line:
            sentenceVector = vectorSum(vector, sentenceVector)
        sentences.append(sentenceVector)
        line = []
    for i in range(0,len(sentences)):
        try:
            emotionalVariance.append(vectorCoolCosine(sentences[i], sentences[i+1]))
            i += 1
        except IndexError:
            break

    file = open('emotionalVariance.txt', 'w')
    fileString = str(emotionalVariance).strip('[]')
    file.write(fileString)
    file.close()