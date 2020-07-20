
import sys
from recommendation import RecommendationEngine
import json


def getModal():
    modal={}
    try:
        with open('data/all.p', 'rb') as fp:
            modal = RecommendationEngine(5,7)
            modal.fit("all")
    except Exception as e:
        print(e)
    return modal


modal=getModal()         
            

def query_recommendation(query):
    wordList=["|start|"]
    wordList.extend(query.split())
    predProb,currProb=modal.predict(wordList)
    resp=[]
    for sent,prob in predProb:
        resp.append({"phrase":sent,"logProbability":prob})      
	print({'query': query, 'prediction' : resp,'phraseLogProbability':currProb })


query_recommendation(sys.argv[1])