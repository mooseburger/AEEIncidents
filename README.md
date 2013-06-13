<a href="http://aeeincidents.info:3000">
  <img src="https://si0.twimg.com/profile_images/3786784212/7e8e30780a549a820e8cf779de9fa5d9_bigger.jpeg" width="48">
</a>
# AEE INCIDENTS
##DEPENDENCIES

Python modules
        
* python-twitter

* python-suds

* python-dateutil

* twilio (easy_install twilio)

node.js

geddy, an MVC framework for node

postgresql

##HOW TO RUN

From a command prompt, change directory into AEEIncidentsApp, and type:
        
` 
geddy &
`

Run electricBreakdowns.py to get the latest breakdowns from the AEE's web service and insert them into the database.

Run postToTwitter.py to post new breakdown reports to your twitter feed.

Send an SMS to 571-414-0557 containing a town (municipio) and an area, separated by comma, to receive an electric breakdown report for your area. 

##LICENSE

AEE INCIDENTS, provides information about incidents via twitter, a map of Puerto Rico and text messages (sms).

This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
