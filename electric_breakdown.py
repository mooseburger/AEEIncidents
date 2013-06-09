import json
import urllib
import dateutil.parser as dparser
from suds.client import Client
aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

#appUrl = "http://23.23.206.79:3000/events"
appUrl = "http://localhost:3000/events"
dateFormat = "%Y-%m-%d %H:%M:00"
snapshot = set()

storedEvents = json.loads(urllib.urlopen(appUrl+".json").read())

for event in storedEvents['events']:
    #print event
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
        #print breakdownArea
        town = breakdownArea.r1TownOrCity.encode("utf-8")
                
        try:
            area = breakdownArea.r2Area.encode("utf-8")
        except UnicodeDecodeError:
            area = breakdownArea.r2Area.decode("utf-8")
            print area

        status = breakdownArea.r3Status.encode("utf-8")
        lastUpdate = breakdownArea.r4LastUpdate.encode("utf-8")
        
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
