import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class NaiveBayes(object):
    def __init__(self):
        self.trainData, self.testData = self.split_train_test_data(0.25)
        self.nbDic = self.trainNB(self.trainData)

    def split_train_test_data(self, test_size):
        print("Spliting Train / Test Data")
        data = pd.read_csv('imdb-ptbr/imdb-reviews-pt-br.csv')
        #data = pd.read_csv('imdb-ptbr/imdb-clear.csv')
        _train_data, _test_data = train_test_split(data, test_size=test_size, shuffle=True)
        return (_train_data, _test_data)

    def clear_strings(self, text):
        newStr = text.replace('.', '')
        newStr = newStr.replace('-', '')
        newStr = newStr.replace(';', '')
        newStr = newStr.replace('\t', '')
        newStr = newStr.replace(',', '')
        newStr = newStr.replace('_', '')

        return newStr.lower()

    def trainNB(self, dataText):
        messageColum = np.array(dataText["text_pt"])
        resultColum = np.array(dataText["sentiment"])
        nbDict = {"pos": {}, "neg": {}}

        print("Starting training...")
        wordsDict = {}
        for i, review in enumerate(messageColum):
            wordsList = review.split()
            wordsDict = nbDict[resultColum[i]]

            for word in wordsList:
                if wordsDict.get(word) == None:
                    wordsDict[word] = 0

                wordsDict[word] += 1

            nbDict[resultColum[i]] = wordsDict
            print("##### progress {:.2f}%..".format((i+1)/len(messageColum)*100), end="\r")

        print("\n##### Finish training model")
        return nbDict

    def calculateWordProb(self, word, wordClass):
        wordClassCount = self.nbDic[wordClass][word] if (self.nbDic[wordClass].get(word) != None) else 0
        Cwords = len(list(self.nbDic[wordClass].keys()))
        arrPos = list(self.nbDic["pos"].keys())
        arrNeg = list(self.nbDic["neg"].keys())
        B = set(arrPos + arrNeg)

        return (wordClassCount + 1.0) / (Cwords + len(B))

    def calculateTextProb(self, text):
        pos = 0
        neg = 0
        entryWords = self.clear_strings(text).split()
        #pos
        pos = len(self.nbDic["pos"])
        neg = len(self.nbDic["neg"])

        print("Calculating sentiment...")
        for i, word in enumerate(entryWords):
            pos *= (self.calculateWordProb(word, "pos") * 1000)
            neg *= (self.calculateWordProb(word, "neg") * 1000)
            print("##### progress {:.2f}%..".format((i+1)/len(entryWords)*100), end="\r")
            
        print("\nFinish Calculating review sentiment")
        print("positive: {0} , Negative: {1}".format(pos, neg))
        return "positive" if pos > neg else "negative"


nb = NaiveBayes()
testText = np.array(nb.testData["text_pt"])[0] 
print("-> Test review is", np.array(nb.testData["sentiment"])[0])
print("\n#### Result ####\nThe review is: ", nb.calculateTextProb(testText))