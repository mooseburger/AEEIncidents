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
	auth_token  = "x"
	client = TwilioRestClient(account_sid, auth_token)
	message = client.sms.messages.create(body=result.status+" en "+result.town+
		" , "+result.area+" "+dparser.parse(result.date, fuzzy = True).strftime(dateFormat),
	to=number,    
	from_="+15714140557")
	return message.sid

appUrl = "http://localhost:3000/messages"
#appUrl = "http://23.23.206.79:3000/messages"
appUrlEvents="http://localhost:3000/events"
#appUrlEvents="http://23.23.206.79:3000/events"

results=[]

storedMessages = json.loads(urllib.urlopen(appUrl+".json").read())
storedEvents= json.loads(urllib.urlopen(appUrlEvents+".json").read())
for message in storedMessages['messages']:
	if(str(message["valid"])=='False'):	
		messageData = message["twBody"]
		#messageData = "san juan, las curias"
		messageLen=len(collections.Counter(messageData.split()))
		#print str(messageLen)
		compareval=""
		for event in storedEvents['events']:

			try:
				area = event["area"].encode("utf-8")
			except UnicodeDecodeError:
				area = event["area"].decode("utf-8")

			#print area
			percent1 = compare_words(messageData,str(area).decode("UTF-8"))
			if(percent1>70):
			    results.append(Result(str(event["id"].encode("UTF-8")),percent1, 
			    	str(event["town"].encode("UTF-8")),str(area).decode("UTF-8"),
			    	str(event["status"].encode("UTF-8")),str(event["lastUpdate"].encode("UTF-8"))))
			#print "1 "+str(percent1) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))
		for event in storedEvents['events']:

			try:
				town = event["town"].encode("utf-8")
			except UnicodeDecodeError:
				town = event["town"].decode("utf-8")

			percent2 = compare_words(messageData,str(town).decode("UTF-8"))
			if(percent2>70):
			    results.append(Result(str(event["id"].encode("UTF-8")),percent2, 
			    	str(event["town"].encode("UTF-8")),str(area).decode("UTF-8"),
			    	str(event["status"].encode("UTF-8")),str(event["lastUpdate"].encode("UTF-8"))))
			#print "2 "+str(percent2) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))
        for event in storedEvents['events']:

			try:
				area = event["area"].encode("utf-8")
				town = event["town"].encode("utf-8")
			except UnicodeDecodeError:
				print "decode"
				area = event["area"].decode("utf-8")
				town = event["town"].decode("utf-8")

			compareval = str(area).decode("UTF-8")
			percent3 = compare_words(messageData,str(town).decode("UTF-8")+" "+compareval)
			if(percent3>75):
				results.append(Result(str(event["id"].encode("UTF-8")),percent3, 
					str(event["town"].encode("UTF-8")),str(area).decode("UTF-8"),
					str(event["status"].encode("UTF-8")),str(event["lastUpdate"].encode("UTF-8"))))
			#print "3 "+str(percent3) +" "+ str(event["area"].encode("UTF-8"))+" "+str(event["town"].encode("UTF-8"))


	if(len(results)>0):
		results=sorted(list(set(results)), key=lambda result: result.percent)
		accurate=results[-1]

		results=sorted(list(set(results)), key=lambda result: result.date)
		recent= results[-1]

		if(accurate.percent>recent.percent):
			finalresult=accurate
		else:
			finalresult=recent
		#print message["twFrom"]	
		print send_sms(message["twFrom"],finalresult)

		#print message["id"]

		url = appUrl + "/" + message["id"] + "?_method=PUT"
		urlParams = urllib.urlencode({"sent":1,"valid":1,"response":str(finalresult.id)})
		response = urllib.urlopen(url, urlParams).read()		
	else:

		url = appUrl + "/" + message["id"] + "?_method=PUT"
    	urlParams = urllib.urlencode({"valid":1})
    	response = urllib.urlopen(url, urlParams).read()

print "Done sending sms"
