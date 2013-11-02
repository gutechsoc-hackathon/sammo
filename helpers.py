import urllib, urllib2, json
#Expects a list of flightIDS
def randFlight(flightIDs):
	random.choice(flightIDS)

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
