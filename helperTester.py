import helpers


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

leavingAirport = 'edi'
destination = 'lgw'
leavingDate = '2013-11-09'
inboundDate = '2013-11-16'
session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, destination, leavingDate, inboundDate=inboundDate)
response = helpers.getLivePriceResponse(session)

print helpers.findCityCountryStart(response)