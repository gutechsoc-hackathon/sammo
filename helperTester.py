import json, helpers, random

# 54.200.253.128:3306

#
## get input from user
## get cities in country 									Michael
## choose a random city from homeCountry					random.choice[cityList]
## get airport IATA codes in cityList 						
## for each airport 										Andrew
## 		open the session with data for that city
## 		get the data
##		if there are no flights available
##			remove IATA code from list of airports
##		else
## 			get the cheapest flight for airport
## output the list of airports and cheapest flight data
#

# con = mdb.connect('54.200.253.128:3306', 'guhack', 'sammo', 'air_data')
# cur = con.cursor()

homeCountry = 'GB'
homeCurrency = 'GBP'
leavingAirport = 'gla'
country = 'UK'
leavingDate = '2013-11-09'
inboundDate = '2013-11-16'

f = open('airportJSON.txt', 'r')
fileString = f.read()
f.close()
airports = json.loads(fileString)


#destination = random.choice(airports['uk']) 
#session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, destination, leavingDate, inboundDate=inboundDate)
#response = helpers.getLivePriceResponse(session)

# print session+'\n'
# print destination + '\n'
# print response['Query']['DestinationPlace']+'\n'
failed = True
while (failed):
	destination = random.choice(airports['uk'])
	print 'destination IATA code ' + destination
	session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, destination, leavingDate, inboundDate=inboundDate)
	response = helpers.getLivePriceResponse(session)
	print 'destination id ' + response['Query']['DestinationPlace']
	failed = len(response['Itineraries']) == 0 

print 'destination code: %s \n destination id: %s \n price: %s \n' % (destination, response['Query']['DestinationPlace'], response['Itineraries'][0]['PricingOptions'][0]['Price'] )
# if (len(response['Itineraries']) != 0 ):
# 	print response['Itineraries'][0]['PricingOptions'][0]['Price']
# else:
# 	print 'no flights available'