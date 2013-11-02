import urllib, urllib2, json
#Expects a list of flightIDS
def randFlight(flightIDs):
	return random.choice(flightIDS)

#Expects a country, the dictionary and a list
def inCountry(country, livePriceResponse, itineraries):
	
	#Start index of the cities type and country types
	cityStart, countryStart = findCityCountryStart(livePriceResponse)

	#for each itineraries currently being considered
	for i in range(len(itineraries)):
		#outboud has the outbound ID
		outbound = livePriceResponse['Itineraries'][i]['OutboundLegId']

		##### FIND THE DESTINATION #####
		#temp is a counter
		temp = 0
		#Loop through the legs until it matches the outbound ID
		while(livePriceResponse['Legs'][temp]['Id'] != outbound
		       and temp<len(livePriceResponse['Legs'])):
			temp++
		#Error checking, will trigger if you have reached end of loop
		#and you haven't found the leg
		if(livePriceResponse['Legs'][temp]['Id'] != outbound):
			print "Error: inCountry, Legs"
			return

		##### FIND THE AIRPORT ##### 
		#Gets the destination ID from the leg you found
		destination = livePriceResponse['Legs'][temp]['DestinationStation']
		#Reset counter
		temp = 0
		#Loops through the places(airports) until you find the destination ID
		while(livePriceResponse['Places'][temp]['Id'] != destination
		       and temp<cityStart):
			temp++
		#Error checking, will trigger if you reach end of loop
		#and you haven't found the destination
		if(livePriceResponse['Places'][temp]['Id'] != destination):
			print "Error: inCountry, Places finding initial Airport"
			return

		##### FIND THE CITY ##### 
		#Grab the parent from the airport, which is the city
		cityID = livePriceResponse['Places'][temp]['ParentId']
		#starts the counter for searching places from where cities begin
		temp = cityStart
		#Loop through the places(cities) until you find the cityID
		while(livePriceResponse['Places'][temp]['Id'] != cityID
		      and temp<countryStart):
			temp++
		#Error checking, will trigger if you reach end of loop
		#and you haven't found city
		if(livePriceResponse['Places'][temp]['Id'] != cityID):
			print "Error: inCountry, Places finding city"
			return

		##### FIND THE COUNTRY ##### 
		#Grab the parent from the city, which is the country
		countryID = livePriceResponse['Places'][temp]['ParentId']
		#Starts the counter for searcgubg places from where countries begin
		temp = countryStart
		#Loop through the countries until you find the countryID
		while(livePriceResponse['Places'][temp]['Id'] != countryID
		      and temp<len(livePriceResponse['Places'])):
			temp++
		#Error checking, will trigger if you reach end of loop
		#and you haven't found country
		if(livePriceResponse['Places'][temp]['Id'] != countryID):
			print "Error: inCountry, Places finding country"
			return		

		##### COMPARE THE CURRENT ITINERARIES COUNTRY WITH USER'S ##### 
		#Grab the country name
		countryName = livePriceResponse['Places'][temp]['Name']
		#If the itinerary country doesnt match the user specified country
		#Remove it from the list
		if(country != countryName):
			itineraries[i] = []

	return itineraries

#Expects a min/max range, the dictionary and a list
def inPriceRange(min, max, livePriceResponse, itineraries):

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
					inboundDate = "", locationSchema = "Iata", cabinClass = "Economy", adults = "1", children = "0", infants = "0"):
	url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'
	values = {	'apikey' : apikey,
				'country' : country,
				'currency' : currency,
				'originplace' : originPlace,
				'destinationplace' : destinationPlace,
				'outbounddate' : outboundDate,
				'locale' : locale,
				'locationschema' : locationSchema,
				'cabinclass' : cabinClass,
				'adults' : adults,
				'children' : children,
				'infants' : infants
			}
	if (inboundDate != ""):
		data[inbounddate] = inboundDate
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' }
	data = urllib.urlencode(values)
	request = urllib2.Request(url, data=data, headers=headers)
	response = urllib2.urlopen(request)
	return response.info().getheader('Location')+'?apikey='+apikey

def getLivePriceResponse(location):
	headers = { 'Content-Type' : 'application/x-www-form-urlencoded' ,
				'Accept' : 'application/json' }
	request = urllib2.Request(location, headers=headers)
	response = urllib2.urlopen(request)
	rawJson = response.read()
	Json = json.loads(rawJson)
	return Json
