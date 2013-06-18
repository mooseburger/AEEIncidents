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


def lookup(town,area, body):
    town = town.lower()
    area = area.lower()
    bodyList=body.lower().split(',')

    if str(bodyList[0]) in town:
        bodylen=len(bodyList)
        if(bodylen==1):
            return 'town'
        elif str(bodyList[bodylen-1]) in area:
            return 'full'
        else:
            return 'town'   
    return 'none'

#this will send a sms for result
def send_sms(number,result):
    dateFormat = "%Y/%m/%d %H:%M:00"
    account_sid = ACCOUNT_SID
    auth_token  = AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    message = client.sms.messages.create(body=result.status+" en "+result.town+
        " , "+result.area+" "+dparser.parse(result.date, fuzzy = True).strftime(dateFormat),
    to=number,    
    from_=TWNUMBER)
    return message.sid

def encodedDict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        out_dict[k] = encodedString(v)
    return out_dict

def encodedString(word):
    if isinstance(word, unicode):
        word = word.encode('utf8')
    elif isinstance(word, str):
        # Must be encoded in UTF-8
        word = word.decode('utf8')
    return word

appUrl = "http://localhost:3000/messages"
appUrlEvents="http://localhost:3000/events"

resultsFull=[]
resultsPartial=[]
storedMessages = json.loads(urllib.urlopen(appUrl+".json").read())
storedEvents= json.loads(urllib.urlopen(appUrlEvents+".json").read())
for message in storedMessages['messages']:
    try:
        message=encodedDict(message)
        if(str(message["valid"])=='False'):    
            messageData = message["twBody"]
            #messageData = "san juan"
            messageLen=len(collections.Counter(messageData.split()))
            
            for event in storedEvents['events']:
                event=encodedDict(event)
                valresult = lookup(str(event["town"]),str(event["area"]), messageData)
                if(valresult=='full'):
                    resultsFull.append(Result(str(event["id"]),valresult, 
                    str(event["town"]),str(event["area"]),
                    str(event["status"]),str(event["lastUpdate"])))
                 
                elif(valresult=='town'):
                    resultsPartial.append(Result(str(event["id"]),valresult, 
                    str(event["town"]),str(event["area"]),
                    str(event["status"]),str(event["lastUpdate"])))

        resultsPartial = sorted(list(set(resultsPartial)), key=lambda result: result.date)
        resultsFull = sorted(list(set(resultsFull)), key=lambda result: result.date)
        
        if(len(resultsFull)>0):
            finalresult=resultsFull[-1]  
        elif(len(resultsPartial)>0):
            finalresult=resultsPartial[-1] 
        else:
            finalresult= None    

    
        if finalresult is not None:
            url = appUrl + "/" + message["id"] + "?_method=PUT"
            urlParams = urllib.urlencode({"sent":1,"valid":1,"response":str(finalresult.id)})
        print send_sms(message["twFrom"],finalresult)            
	    response = urllib.urlopen(url, urlParams).read() 
        else:
            url = appUrl + "/" + message["id"] + "?_method=PUT"
            urlParams = urllib.urlencode({"valid":1,"response":str("not valid input")})
            response = urllib.urlopen(url, urlParams).read() 
        print finalresult
    except Exception:
        print event
        url = appUrl + "/" + message["id"] + "?_method=PUT"
        urlParams = urllib.urlencode({"valid":1,"response":str("not valid input")})
        response = urllib.urlopen(url, urlParams).read() 
        continue
print "Done sending sms"
