DEPENDENCIES

    Python modules
        
        python-twitter

        python-suds

        python-dateutil

        twilio (easy_install twilio)

node.js

geddy, an MVC framework for node

postgresql

HOW TO RUN

    From a command prompt, change directory into AEEIncidentsApp, and type:
        
        geddy

    Run electricBreakdowns.py to get the latest breakdowns from the AEE's web service and insert them into the database.

    Run postToTwitter.py to post new breakdown reports to your twitter feed.

    Send an SMS to 571-414-0557 containing a town (municipio) and an area, separated by comma, to receive an electric breakdown report for your area. 