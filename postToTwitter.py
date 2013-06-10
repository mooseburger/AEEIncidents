import twitter
import json
import urllib
import dateutil.parser as dparser

#appUrl = "http://23.23.206.79:3000/events"
appUrl = "http://localhost:3000/events"
dateFormat = "%m/%d/%Y %I:%M:00 %p"

tweetFormat = "{Fecha}: Incidente reportado en {Area}, #{Municipio} - Estado: {Estado}" 

jsonData = json.loads(urllib.urlopen(appUrl+".json").read())

latestEvents = jsonData["events"]
eventsToPost = [event for event in latestEvents if not event["posted"]]

twitterApi = twitter.Api(consumer_key="NCgdH3VLp5MGcCtvqBcEg",
                         consumer_secret="ws9gH3IMMf7Me3yisICjRbog4Irove05PTMkBv1e8",
                         access_token_key="1486306525-RGwIIsWXfWlRiUTqQlSB6f1icA5ZTd806E3X1tz",
                         access_token_secret="aZX45fWxpkdHa6ddHtEd4VHUamXzXEHkvVb174Mk")

for event in eventsToPost:
    lastUpdate = dparser.parse(event["lastUpdate"], fuzzy = True).strftime(dateFormat)
    
    try:    
        area = event["area"].encode("utf-8")
    except UnicodeDecodeError:
        area = event["area"].decode("utf-8")

    town =  event["town"].decode("utf-8")
    status = event["status"].decode("utf-8")    
  
    town = "".join(town.split())
    
    tweet = tweetFormat.format(Fecha=lastUpdate, Area=area, Municipio=town, Estado=status)
    twitterApi.PostUpdate(tweet)

    url = appUrl + "/" + event["id"] + "?_method=PUT"
        
    urlParams = urllib.urlencode({"posted":1})
    #print tweet    
    #print url + urlParams    
    response = urllib.urlopen(url, urlParams).read()
    
    


