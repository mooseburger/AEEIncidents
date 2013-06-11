import twitter
import json
import urllib
import dateutil.parser as dparser

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
    try:
        event = encodedDict(event)        
        lastUpdate = dparser.parse(event["lastUpdate"], fuzzy = True).strftime(dateFormat)
    
        area = event["area"]

        town =  event["town"]
        status = event["status"]    
  
        town = "".join(town.split())
    
        tweet = tweetFormat.format(Fecha=lastUpdate, Area=area, Municipio=town, Estado=status)
        try:
            twitterApi.PostUpdate(tweet)
        except twitter.TwitterError:
            pass #something goes wrong on post we don't want to tweet that again
        
        url = appUrl + "/" + event["id"] + "?_method=PUT"
        
        urlParams = urllib.urlencode({"posted":1})
        #print tweet    
        #print url + urlParams    
        response = urllib.urlopen(url, urlParams).read()
    except Exception:
        continue
