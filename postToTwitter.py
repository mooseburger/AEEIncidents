import twitter
import json
import urllib
import dateutil.parser as dparser
from config import *
from encodingHelper import *

#appUrl = "http://aeeincidents.info:3000/events"
appUrl = "http://localhost:3000/events"
dateFormat = "%m/%d/%Y %I:%M:00 %p"

tweetFormat = "{Fecha}: Incidente reportado en {Area}, #{Municipio} - Estado: {Estado}" 

jsonData = json.loads(urllib.urlopen(appUrl+".json").read())

latestEvents = jsonData["events"]
eventsToPost = [event for event in latestEvents if not event["posted"]]

twitterApi = twitter.Api(consumer_key = CONSUMER_KEY,
                         consumer_secret = CONSUMER_SECRET,
                         access_token_key = ACCESS_TOKEN,
                         access_token_secret = ACCESS_TOKEN_SECRET)

for event in reversed(eventsToPost):
    try:
        event = encodedDict(event)        
        lastUpdate = dparser.parse(event["lastUpdate"], fuzzy = True).strftime(dateFormat)
    
        area = event["area"]

        town =  event["town"]
        status = event["status"]    
  
        town = "".join(town.split())
    
        tweet = tweetFormat.format(Fecha = lastUpdate, Area = area, Municipio = town, Estado = status)
        try:
            twitterApi.PostUpdate(tweet)
        except twitter.TwitterError:
            print tweet
            pass #something goes wrong on post we don't want to tweet that again
        
        url = appUrl + "/" + event["id"] + "?_method=PUT"
        
        urlParams = urllib.urlencode({"posted":1})
        #print tweet    
        #print url + urlParams    
        response = urllib.urlopen(url, urlParams).read()
    except Exception:
        print event
        continue
