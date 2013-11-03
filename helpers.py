import urllib, urllib2, json, random, MySQLdb as mdb

## for each airport
##      open the session with data for that city
##      get the data
##      if there are no flights available
##          remove IATA code from list of airports
##      else
##          get the cheapest flight for airport and info of flight

con = mdb.connect('54.200.253.128:3306', 'guhack', 'sammo', 'air_data')
cur = con.cursor()

def run(input):
	cities = getCities(input['CountryTravellingTo'])
	destination = randomCity(cities)
	iataCodes = getIATAcodes(destination)
	airportData['destination'] = destination
	airportData['prices'] = {}
	for row in iataCodes:
		if (row[0] != ''):
			airportData[row[0]] = {}
	findMinFlightCosts(airportData['prices'], input['HomeCountry'], input['AirportLeavingFrom'], input['DepartureDate'])
	return airportData



#Gets the cheapest flight to each airport
def findMinFlightCost(dictionaryOfIATA, homeCountry, homeCurrency, leavingAirport, leavingDate):
    for IATA in dictionaryOfIATA.keys():
        session = helpers.createSession(homeCountry, homeCurrency, leavingAirport, IATA, leavingDate)
        response = helpers.getLivePriceResponse(session)
        if(len(response['Itineraries']) == 0):
            del dictionaryOfIATA[IATA]
        else:
            dictionaryOfIATA[IATA]['Price'] = response['Itineraries'][0]['PricingOptions'][0]['Price']

            ##### FIND THE CARRIER ###
            #outboud has the outbound ID
            outbound = response['Itineraries'][IATA]['OutboundLegId']
            #Get the index of the leg that matches the outboundID
            legIndex = getID(response['Legs'], outbound)
            if(legIndex < 0):
                return -1
            #Get the departure time from the leg
            dictionaryOfIATA[IATA]['DepartureTime'] = response['Legs'][legIndex]['Departure']
            
            #Get the carrier ID from the leg
            carrierID = response['Legs'][legIndex]['Carriers'][0]
            #Get the index of the carrier that matches the carrierID
            carrierIndex = getID(response['Carriers'], carrierID)
            if(carrierIndex < 0):
                return  -1
            #Get the Carrier's Name and Image
            dictionaryOfIATA[IATA]['CarrierName'] = response['Carriers'][carrierIndex]['Name']
            dictionaryOfIATA[IATA]['CarrierURL'] = response['Carriers']['ImageUrl']

    return dictionaryOfIATA

# Pass in a list that you wish to search for the ID
def getID(list, ID):
    counter = 0
    #Loop through the legs until it matches the outbound ID
    while(list[counter]['Id'] != ID and counter<len(list)):
        counter+=1
    #Error checking, will trigger if you have reached end of loop
    #and you haven't found the leg
    if(list[counter]['Id'] != ID):
        print "Error: getID, " + ID
        return -1
    return counter            



def createSession(country, originPlace, destinationPlace, outboundDate, currency='GBP', apikey="hck55686622578671415146356618825", locale="en-GB",\
                                        inboundDate = "", locationSchema = "Iata", cabinClass = "Economy", adults = "1", children = "0", infants = "0"):
        url = 'http://partners.api.skyscanner.net/apiservices/pricing/v1.0'
        values = {      'apikey' : apikey,
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
                values['inboundate'] = inboundDate
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

#Expects a max range, the dictionary and a sorted list(by price)
def inPriceRange(max, livePriceResponse, itineraries):
    counter = 0
    for i in itineraries:
        if (max < livePriceResponse['Itineraries'][i]['PricingOptions'][0]['Price']):
            itineraries[i] = []
    return itineraries
        
def getCities(country):
	cur.execute("SELECT City FROM Locations WHERE Country = '" + countryStart "'")
	c cur.fetchall()
	return c

def getIATAcodes(city):
	cur.execute("SELECT Iata FROM Locations WHERE City = '" + city + "'")
	c cur.fetchall()
	return c

def randomCity(cities):
	return random.choice(cites)[0]

# DEPRECATED
# #Expects a country, the dictionary and a list
# #Modifies the itineraries list to remove the itineraries that
# #don't match the country
# def inCountry(country, livePriceResponse, itineraries):
        
#         #Start index of the cities type and country types
#         cityStart, countryStart = findCityCountryStart(livePriceResponse)

#         #for each itineraries currently being considered
#         for i in itineraries:
#                 #outboud has the outbound ID
#                 outbound = livePriceResponse['Itineraries'][i]['OutboundLegId']

#                 ##### FIND THE DESTINATION #####
#                 #temp is a counter
#                 temp = 0
#                 #Loop through the legs until it matches the outbound ID
#                 while(livePriceResponse['Legs'][temp]['Id'] != outbound\
#                         and temp<len(livePriceResponse['Legs'])):
#                         temp+=1
#                 #Error checking, will trigger if you have reached end of loop
#                 #and you haven't found the leg
#                 if(livePriceResponse['Legs'][temp]['Id'] != outbound):
#                         print "Error: inCountry, Legs"
#                         return

#                 ##### FIND THE AIRPORT ##### 
#                 #Gets the destination ID from the leg you found
#                 destination = livePriceResponse['Legs'][temp]['DestinationStation']
#                 #Reset counter
#                 temp = 0
#                 #Loops through the places(airports) until you find the destination ID
#                 while(livePriceResponse['Places'][temp]['Id'] != destination\
#                         and temp<cityStart):
#                         temp+=1
#                 #Error checking, will trigger if you reach end of loop
#                 #and you haven't found the destination
#                 if(livePriceResponse['Places'][temp]['Id'] != destination):
#                         print "Error: inCountry, Places finding initial Airport"
#                         return

#                 ##### FIND THE CITY ##### 
#                 #Grab the parent from the airport, which is the city
#                 cityID = livePriceResponse['Places'][temp]['ParentId']
#                 #starts the counter for searching places from where cities begin
#                 temp = cityStart
#                 #Loop through the places(cities) until you find the cityID
#                 while(livePriceResponse['Places'][temp]['Id'] != cityID\
#                         and temp<countryStart):
#                         temp+=1
#                 #Error checking, will trigger if you reach end of loop
#                 #and you haven't found city
#                 if(livePriceResponse['Places'][temp]['Id'] != cityID):
#                         print "Error: inCountry, Places finding city"
#                         return

#                 ##### FIND THE COUNTRY ##### 
#                 #Grab the parent from the city, which is the country
#                 countryID = livePriceResponse['Places'][temp]['ParentId']
#                 #Starts the counter for searcgubg places from where countries begin
#                 temp = countryStart
#                 #Loop through the countries until you find the countryID
#                 while(livePriceResponse['Places'][temp]['Id'] != countryID\
#                         and temp<len(livePriceResponse['Places'])):
#                         temp+=1
#                 #Error checking, will trigger if you reach end of loop
#                 #and you haven't found country
#                 if(livePriceResponse['Places'][temp]['Id'] != countryID):
#                         print "Error: inCountry, Places finding country"
#                         return          

#                 ##### COMPARE THE CURRENT ITINERARIES COUNTRY WITH USER'S ##### 
#                 #Grab the country name
#                 countryName = livePriceResponse['Places'][temp]['Name']
#                 #If the itinerary country doesnt match the user specified country
#                 #Remove it from the list
#                 if(country != countryName):
#                         itineraries[i] = []

#         return itineraries

# DEPRECATED
# #Finds the starting positions onf the place types City and Country
# def findCityCountryStart(livePriceResponse):
#         cityStart = 0
#         countryStart = 0
#         temp = 0
#         while(country==0 and temp<len(livePriceResponse['Places'])):
#                 if(livePriceResponse['Places'][temp]['Type'] == "City"):
#                         cityStart = temp
#                 if(livePriceResponse['Places'][temp]['Type'] == "Country"):
#                         countryStart = temp
#                 temp+=1
        
#         if(cityStart==0 or countryStart==0):
#                 print "Error findCityCountryStart"
#                 return None
        
#         return cityStart, countryStart
