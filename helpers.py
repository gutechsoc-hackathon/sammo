import urllib2, json

#Expects a list of flightIDS
def randFlight(flightIDs):
	return random.choice(flightIDS)

#Expects a country, the dictionary and a list
def inCountry(country, livePriceResponse, itineraries):
	
	cityStart, countryStart = findCityCountryStart(livePriceResponse)

	for i in range(len(itineraries)):
		outbound = livePriceResponse['Itineraries'][i]['OutboundLegId']

		temp = 0
		while(livePriceResponse['Legs'][temp]['Id'] != outbound
		       and temp<len(livePriceResponse['Legs'])):
			temp++
		
		if(livePriceResponse['Legs'][temp]['Id'] != outbound):
			print "Error: inCountry, Legs"
			return

		destination = livePriceResponse['Legs'][temp]['DestinationStation']
		temp = 0
		while(livePriceResponse['Places'][temp]['Id'] != destination
		       and temp<len(livePriceResponse['Places'])):
			temp++

		if(livePriceResponse['Places'][temp]['Id'] != destination):
			print "Error: inCountry, Places finding initial Airport"
			return

		cityID = livePriceResponse['Places'][temp]['ParentId']
		temp = cityStart
		while(livePriceResponse['Places'][temp]['Id'] != cityID
		      and temp<len(livePriceResponse['Places'])):
			temp++

		if(livePriceResponse['Places'][temp]['Id'] != cityID):
			print "Error: inCountry, Places finding city"
			return

		countryID = livePriceResponse['Places'][temp]['ParentId']
		temp = countryStart
		while(livePriceResponse['Places'][temp]['Id'] != countryID
		      and temp<len(livePriceResponse['Places'])):
			temp++

		if(livePriceResponse['Places'][temp]['Id'] != countryID):
			print "Error: inCountry, Places finding country"
			return		

		countryName = livePriceResponse['Places'][temp]['Name']
		if(country != countryName):
			list[i] = []

	return itineraries

#Expects a min/max range, the dictionary and a list
def inPriceRange(min, max, dictionary, list):

	return list


#Finds the starting positions onf the place types City and Country
def findCityCountryStart(livePriceResponse):
	cityStart = 0
	countryStart = 0
	temp = 0
	while(country==0 and temp<len(livePriceResponse['Places'])):
		if(livePriceResponse['Places'][temp]['Type'] == "City"):
			cityStart = temp
		if(livePriceResponse['Places'][temp]['Type'] == "Country"):
			countryStart = temp
		temp++
	
	if(cityStart==0 or countryStart==0):
		print "Error findCityCountryStart"
		return None
	
	return cityStart, countryStart

def createSession(apikey, country, currency, originPlace, destinationPlace, outboundDate, locale="en-GB",\
					inboundDate = "", locationSchema = "lata", cabinClass = "Economy", adults = "1", children = "0", infants = "0"):
	url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'
	data = {'apikey' : apikey,
			'country' : country,
			'locale' : locale,
			'originplace' : originPlace,
			'destinationplace' : destinationPlace,
			'outbounddate' : outboundDate,
			'locationschema' : locationSchema,
			}
	if (inboundDate != ""):
		data[inbounddate] = inboundDate
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' ,
				'Accept' : 'applicton/json' }
	request = urllib2.request(url, data=data, headers=headers)
	response = urllib2.urlopen(request)
	print response.info().getheader('Location')
	return response.info().getheader('Location')

def getLivePriceResponse(location):
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' ,
				'Accept' : 'applicton/json' }
	request = urllib2.request(url, headers=headers )
	response = urllib2.urlopen(request)
	rawJson = response.read()
	Json = json.loads(rawJson)
