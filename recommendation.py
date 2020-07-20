import numpy as np
import pandas as pd
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
import json


class CurrPredictTreeNode: 
    def __init__(self,prob_tree,wordList,lastIndex=0,prob=None):
        self.prob_tree=prob_tree
        self.wordList=wordList
        self.prob=prob
        self.lastIndex=lastIndex
        self.child=None
           
        
    def getProbability(self):
        if self.lastIndex+3 <= len(self.wordList):
            self.trigram = self.wordList[self.lastIndex:self.lastIndex+3]
            try:
                if self.prob==None:
                    self.prob=np.log(self.prob_tree[self.trigram[0]][self.trigram[1]][self.trigram[2]]["prob"])
                else:
                    self.prob+=np.log(self.prob_tree[self.trigram[0]][self.trigram[1]][self.trigram[2]]["prob"])
                self.child = CurrPredictTreeNode(self.prob_tree, self.wordList, self.lastIndex+1,self.prob)
                return self.child.getProbability()
            except Exception as e:
                print(e,"error")
                return None
        else:
            return self.prob
        

class PredictTreeNode:
    def __init__(self, prob_tree, wordList, max_search=3, max_depth=5,prob=None,sentence=""):
        self.prob_tree = prob_tree
        self.wordList = wordList
        self.max_depth = max_depth
        self.max_search = max_search
        self.prob = prob
        self.sentence=sentence
        
        if len(self.wordList) >= 2:
            self.prev_word = self.wordList[-2:][0]
            self.curr_word = self.wordList[-2:][1]
            
            
    def getPredictedData(self):
        if len(self.wordList) >= 2 and self.max_depth-1 >=0 and self.prev_word in self.prob_tree and self.curr_word in self.prob_tree[self.prev_word]:
            self.next_nodes = self.prob_tree[self.prev_word][self.curr_word]
            self.next_nodes_prob = []
            self.next_nodes_word = []
            for key,value in self.next_nodes.items():
                self.next_nodes_word.append(key)
                self.next_nodes_prob.append(value['prob'])
            self.next_nodes_prob= np.asarray(self.next_nodes_prob)
            self.next_nodes_word= np.asarray(self.next_nodes_word)
            sorted_node_prob_index = np.argsort(-self.next_nodes_prob)
            if len(sorted_node_prob_index) > self.max_search:
                sorted_node_prob_index = sorted_node_prob_index[:self.max_search]
            self.next_nodes_prob=np.log(self.next_nodes_prob[sorted_node_prob_index])
            self.next_nodes_word=self.next_nodes_word[sorted_node_prob_index]
            sentences=[]
            for i,word in enumerate(self.next_nodes_word):
                if self.prob==None:
                    prob=self.next_nodes_prob[i]
                else:
                    prob=self.prob+self.next_nodes_prob[i]
                sentence=self.sentence+" " +self.curr_word+" "
                predict_prob=PredictTreeNode(self.prob_tree, [self.curr_word, word], 5, self.max_depth-1,prob,sentence)
                sentences.extend(predict_prob.getPredictedData())
            return list(set(sentences))
                
        else:
            return [(" ".join(self.sentence.split()[1:]),self.prob)]
        
class RecommendationEngine:
    def __init__(self,search=5,depth=5):
        self.tree = {}
        self.prob_tree={}
        self.search=search
        self.depth=depth

    def fit(self,projectId):  
        # with open('data/'+projectId+'.json', 'r') as fp:
        #     self.prob_tree= json.load(fp)
        with open('data/'+projectId+'.p', 'rb') as f:
            self.prob_tree= pickle.load(f)
    
    def predict(self,wordList):
        self.curr_prob_tree=CurrPredictTreeNode(self.prob_tree, wordList)
        curr_prob=self.curr_prob_tree.getProbability()
        predict_prob=PredictTreeNode(self.prob_tree, wordList, self.search, self.depth)
        sentences = []
        probs = []
        for (sentence, prob) in predict_prob.getPredictedData():
            probs.append(prob)
            sentences.append(sentence)
        sentences = np.asarray(sentences)
        probs = np.asarray(probs)
        sortedProbs = np.argsort(-probs)
        sentences = sentences[sortedProbs]
        probs=probs[sortedProbs]
        sentences=sentences[sortedProbs]
        return zip(sentences,probs),curr_prob

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



        
        
