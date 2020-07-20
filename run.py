
import sys
from recommendation import RecommendationEngine
import json


def getModal():
    data=[]
    modal={}
    with open('data/queryCleanData.json', 'r') as fp:
        queryData= json.load(fp)
    keysQuery=[]
    keysQuery.extend(list(queryData.keys()))
    print(keysQuery)
    for projectId in keysQuery:
        try:
            with open('data/'+projectId+'.p', 'rb') as fp:
                reco = RecommendationEngine(5,7)
                reco.fit(projectId)
                modal[projectId]=reco
        except Exception as e:
            print(e)
    return modal


modal=getModal()         
            

def query_recommendation(projectId,query):
	if projectId in modal:
		reco=modal[projectId]
		wordList=["|start|"]
		wordList.extend(query.split())
		predProb,currProb=reco.predict(wordList)
		resp=[]
		for sent,prob in predProb:
			resp.append({"phrase":sent,"logProbability":prob})      
	print({'query': query, 'prediction' : resp,'phraseLogProbability':currProb })


query_recommendation(sys.argv[1],sys.argv[2])