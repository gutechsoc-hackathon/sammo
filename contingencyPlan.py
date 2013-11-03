#import helpers

import json
# input = {	'countryTo' : 'Spain',
# 			'departDate' : '2013-12-20',
# 			'leavingAirport': 'GLA' }
# response = run(input)

# print response
f = open('air_data.json', 'r')
fileString = f.read()
f.close()
data = json.loads(fileString)

count = 0

for row in data:
	count+=1

print count