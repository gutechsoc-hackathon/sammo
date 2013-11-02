import json, helpers, random


## get country data
## get home country from user
## get currency from user
## get leaving airport from user
## get country traveling to from user
## get leaving date from user
## choose a random city from country
## open the session with data for that city
## get the data
## get the cheapest flight for each airport in that city
## output the data

countryData = 0 ##Pretend this is the json of country:cities
homeCountry = 'GB'
homeCurrency = 'GBP'
leavingAirport = 'gla'
country = 'UK'
leavingDate = '2013-12-06'
##randomCity = randFlight(countryData[country])

#session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, 'Man', leavingDate, inboundDate='2013-12-07')
# response = helpers.getLivePriceResponse(session)
# print session+'\n'
# print response
# print session+'\n'

f = open('airportJSON.txt', 'r')
fileString = f.read()
f.close()
airports = json.loads(fileString)

#print random.choice(airports['uk'])

leavingAirport = 'edi'
destination = random.choice(airports['uk'])
leavingDate = '2013-11-09'
inboundDate = '2013-11-16'
 
session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, destination, leavingDate, inboundDate=inboundDate)
response = helpers.getLivePriceResponse(session)

print session
print destination + '\n'
print response['Query']['DestinationPlace']+'\n'
if (len(response['Itineraries']) != 0 ):
	print response['Itineraries'][0]['PricingOptions'][0]['Price']