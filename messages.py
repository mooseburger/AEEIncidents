import json
import urllib
import re
import collections
import dateutil.parser as dparser
from suds.client import Client
from twilio.rest import TwilioRestClient

class Result:
        def __init__(self, id, percent, town, area,status,date):
                self.id = id
                self.percent = percent
                self.town = town
                self.area= area
                self.status=status
                self.date=date
        def __repr__(self):
                return repr((self.id, self.percent, self.town, self.area, self.status, self.date))

#this will compare two sentences and return the percentage of exact words contained in the second sentence
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

#this will send a sms for result
def send_sms(number,result):
	dateFormat = "%Y/%m/%d %H:%M:00"
	account_sid = "ACa0ab47de030b424a97788cec56ab466c"
	auth_token  = "4de19bdeb9061152e7c5c97da876e26e"
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(body=result.status+" en "+result.town+
		" , "+result.area+" "+dparser.parse(result.date, fuzzy = True).strftime(dateFormat),
	to=number,    
	from_="+15714140557")
	return message.sid

aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

appUrl = "http://23.23.206.79:3000/messages"

results=[]

storedMessages = json.loads(urllib.urlopen(appUrl+".json").read())
storedEvents= json.loads(urllib.urlopen("http://23.23.206.79:3000/events.json").read())
for message in storedMessages['messages']:
	if(str(message["valid"])=='False'):	
		messageData = message["twBody"]
		messageData = "san juan, las curias"
		messageLen=len(collections.Counter(messageData.split()))
		#print str(messageLen)
		compareval=""
		for event in storedEvents['events']:
			percent1 = compare_words(messageData,str(event["area"].decode("UTF-8")))
			if(percent1>70):
			    results.append(Result(str(event["id"].decode("UTF-8")),percent1, 
			    	str(event["town"].decode("UTF-8")),str(event["area"].decode("UTF-8")),
			    	str(event["status"].decode("UTF-8")),str(event["lastUpdate"].decode("UTF-8"))))
			#print "1 "+str(percent1) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))
		for event in storedEvents['events']:
			percent2 = compare_words(messageData,str(event["town"].decode("UTF-8")))
			if(percent2>70):
			    results.append(Result(str(event["id"].decode("UTF-8")),percent2, 
			    	str(event["town"].decode("UTF-8")),str(event["area"].decode("UTF-8")),
			    	str(event["status"].decode("UTF-8")),str(event["lastUpdate"].decode("UTF-8"))))
			#print "2 "+str(percent2) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))
        for event in storedEvents['events']:
			compareval = str(event["area"].decode("UTF-8"))
			percent3 = compare_words(messageData,str(event["town"].decode("UTF-8"))+" "+compareval)
			if(percent3>75):
				results.append(Result(str(event["id"].decode("UTF-8")),percent3, 
					str(event["town"].decode("UTF-8")),str(event["area"].decode("UTF-8")),
					str(event["status"].decode("UTF-8")),str(event["lastUpdate"].decode("UTF-8"))))
			#print "3 "+str(percent3) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))


	results=sorted(list(set(results)), key=lambda result: result.percent)
	accurate=results[-1]

	results=sorted(list(set(results)), key=lambda result: result.date)
	recent= results[-1]

	if(accurate.percent>recent.percent):
		finalresult=accurate
	else:
		finalresult=recent
	#messageData = message["twTo"]
	print send_sms("+17872190992",finalresult)

print "Done polling our database"
