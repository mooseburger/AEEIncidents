import urllib
from suds.client import Client
aee_url = 'http://wss.prepa.com/services/BreakdownReport?wsdl'
aee_client = Client(aee_url)
breakdownSummary = aee_client.service.getBreakdownsSummary()

for summary in breakdownSummary:
	print summary.r1TownOrCity
	breakdowns = aee_client.service.getBreakdownsByTownOrCity(summary.r1TownOrCity)
	for breakdownArea in breakdowns:
		print breakdownArea 
		data = urllib.urlencode({"town" : breakdownArea.r1TownOrCity.encode("utf-8"), "area" : breakdownArea.r2Area.encode("utf-8"), "status" : breakdownArea.r3Status.encode("utf-8"), "lastUpdate" : breakdownArea.r4LastUpdate.encode("utf-8")})
		postResult = urllib.urlopen("http://ec2-50-19-196-16.compute-1.amazonaws.com:4000/tickets/", data).read()