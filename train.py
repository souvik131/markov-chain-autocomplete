import numpy as np
import pandas as pd
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
import json

    
class RecommendationEngine:
    def __init__(self,search=5,depth=5):
        self.tree = {}
        self.prob_tree={}
        self.search=search
        self.depth=depth

    def save(self,projectId,data):  
        print(projectId,len(data)," total length")
        for i,el in enumerate(data):
            sentence=el[0]
            count=el[1]
            result=['|start|']
            result.extend(sentence.lower().strip().split(" "))    
            result.extend(['|end|'])
            self.trace(result,count)
            if i%2000==0:
                print(str(i)+"th iteration")
                print(len(self.tree.keys()), "words")
        self.calculate()
        with open('data/'+projectId+'.p', 'wb') as fp:
            pickle.dump(self.prob_tree, fp, protocol=pickle.HIGHEST_PROTOCOL)
        with open('data/'+projectId+'.json', 'w') as fp:
            json.dump(self.prob_tree, fp)

    def trace(self, wordList,wordCount):
        if not self.tree:
            self.tree = {}
        for i,word in enumerate(wordList):
            newFlag=False
            if len(wordList)-1 != i:
                if wordList[i-1] not in self.tree:
                    self.tree[wordList[i-1]] = {}
                if word not in self.tree[wordList[i-1]]:
                    self.tree[wordList[i-1]][word] = {}
                if wordList[i+1] not in self.tree[wordList[i-1]][word]:
                    self.tree[wordList[i-1]][word][wordList[i+1]] = wordCount
                    newFlag=True
                if not newFlag:
                    self.tree[wordList[i-1]][word][wordList[i+1]] += wordCount
        self.tree.pop('|end|', None)

    def calculate(self):
        for prevWord, childData in self.tree.items():
            for currWord, grandChildData in childData.items():
                total=0
                for nextWord, count in grandChildData.items():
                    total+=count
                for nextWord, count in grandChildData.items():
                    if prevWord not in self.prob_tree:
                        self.prob_tree[prevWord]={}
                    if currWord not in self.prob_tree[prevWord]:
                        self.prob_tree[prevWord][currWord]={}
                    self.prob_tree[prevWord][currWord][nextWord]={
                        "freq":count,
                        "prob":count/total
                    }




def runAll():
    with open('data/queryCleanData.json', 'r') as fp:
        queryData= json.load(fp)
    dataset=[]
    for phrase, count in queryData.items():
        dataset.append((phrase, count))
    reco = RecommendationEngine(5,7)
    reco.save('all',dataset)

runAll()
#run()


         
            

        
        
