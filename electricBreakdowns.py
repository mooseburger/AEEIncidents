import json
import urllib
import dateutil.parser as dparser
from suds.client import Client
aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

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

#appUrl = "http://aeeincidents.info:3000/events"
appUrl = "http://localhost:3000/events"
dateFormat = "%Y-%m-%d %H:%M:00"
snapshot = set()

storedEvents = json.loads(urllib.urlopen(appUrl+".json").read())

for event in storedEvents["events"]:
    
    event = encodedDict(event)    
    
    eventData = event["town"] + event["area"] + event["status"]
    jsonLastUpdate = dparser.parse(event["lastUpdate"], fuzzy = True).strftime(dateFormat)
    eventData = eventData + jsonLastUpdate
    
    eventId = "".join(eventData.lower().split())
    snapshot.add(eventId)

#print snapshot.keys()
print "Done polling our database"

breakdownSummary = aee_client.service.getBreakdownsSummary()

for summary in breakdownSummary:
    #print summary.r1TownOrCity
    breakdowns = aee_client.service.getBreakdownsByTownOrCity(summary.r1TownOrCity)
    for breakdownArea in breakdowns:
        try:        
            print breakdownArea
            town = encodedString(breakdownArea.r1TownOrCity)
                    
            area = encodedString(breakdownArea.r2Area)
            
            status = encodedString(breakdownArea.r3Status)
            lastUpdate = encodedString(breakdownArea.r4LastUpdate)
            
            updateDate = dparser.parse(lastUpdate, fuzzy = True)
            lastUpdate = updateDate.strftime(dateFormat)
            #print lastUpdate
            identifyingData = town + area + status + lastUpdate
            relevantData = "".join(identifyingData.lower().split())
        
            if not relevantData in snapshot:
                print identifyingData
                urlParams = {"town" : town, "area" : area, "status" : status, "lastUpdate" : lastUpdate}
                
                data = urllib.urlencode(urlParams)
                                         
                postResult = urllib.urlopen(appUrl, data).read()
        except:
            continue
