import urllib2, json

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