
import sys

def query_recommendation(projectId,query):
	if projectId in modal:
		reco=modal[projectId]
		wordList=["|start|"]
		wordList.extend(query.split())
		predProb,currProb=reco.predict(wordList)
		resp=[]
		for sent,prob in predProb:
			resp.append({"phrase":sent,"logProbability":prob})      
	print({'query': request.json['query'], 'prediction' : resp,'phraseLogProbability':currProb })


query_recommendation(sys.argv[1],sys.argv[2])