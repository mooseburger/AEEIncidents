import json
import urllib
import dateutil.parser as dparser
from suds.client import Client
aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)

appUrl = "http://ec2-23-23-46-186.compute-1.amazonaws.com:4000/events"

snapshot = {}

storedEvents = json.loads(urllib.urlopen(appUrl+".json").read())

for event in storedEvents['events']:
	eventData = event["town"] + event["area"] + event["status"]
	#print eventData
	cleanData = "".join(eventData.lower().split())
	#breakdownHash = hashlib.md5()
	#breakdownHash.update(cleanData);
	snapshot[cleanData] = eventData

print "Done polling our database"
breakdownSummary = aee_client.service.getBreakdownsSummary()

for summary in breakdownSummary:
	#print summary.r1TownOrCity
	breakdowns = aee_client.service.getBreakdownsByTownOrCity(summary.r1TownOrCity)
	for breakdownArea in breakdowns:
		#print breakdownArea 
		town = breakdownArea.r1TownOrCity.decode("utf-8")
		area = breakdownArea.r2Area.decode("utf-8")
		status = breakdownArea.r3Status.decode("utf-8")
		lastUpdate = breakdownArea.r4LastUpdate.decode("utf-8")

		relevantData = "".join((town + area + status).lower().split())

		updateDate = dparser.parse(lastUpdate, fuzzy = True)
		lastUpdate = updateDate.strftime("%Y-%m-%d %H:%M:00")
		if not snapshot.has_key(relevantData):
			#print breakdownArea
			#print town + area + status + lastUpdate
			data = urllib.urlencode({"town" : town, "area" : area, "status" : status, "lastUpdate" : lastUpdate})
			postResult = urllib.urlopen(appUrl, data).read()