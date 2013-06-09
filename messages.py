import json
import urllib
import re
import collections
import dateutil.parser as dparser
from suds.client import Client

def compare_words(sentence1, sentence2):
	matches=0;
	splitter = re.compile(r'(\s+|\S+)')
	splitedSentence1 = splitter.findall(sentence1.lower().replace(","," "))
	#print splitedSentence1
	#print "compared:" + sentence2
	wordLen1=range(len(splitedSentence1))
	for i in wordLen1:
		if splitedSentence1[i] in sentence2.lower():
			matches+=1
	similarity = (100*matches)/len(wordLen1)
	return similarity

aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

appUrl = "http://23.23.206.79:4000/messages"

dateFormat = "%Y-%m-%d %H:%M:00"
snapshot = {}

storedMessages = json.loads(urllib.urlopen(appUrl+".json").read())
locations= json.loads(urllib.urlopen("http://localhost:4000/locations.json").read())
for message in storedMessages['messages']:
	if(str(message["valid"])=='False'):	
		messageData = message["twBody"]
		messageData = "bayamon monterey"
		messageLen=len(collections.Counter(messageData.split()))
		#print str(messageLen)
		compareval=""
		for location in locations['locations']:
			if(int(messageLen)>2 & str(messageData[:3]).lower()!="san"):
				compareval = str(location["barrio"].encode("UTF-8"))
			result = compare_words(messageData,str(location["municipio"].encode("UTF-8"))+" "+compareval)
			if(result>80):
				print str(result) +" "+ str(location["municipio"].encode("UTF-8"))+" "+str(location["barrio"].encode("UTF-8"))
print "Done polling our database"
