import helpers

input = {	'countryTo' : 'Spain',
			'departDate' : '2013-12-20',
			'leavingAirport': 'GLA' }
#response = helpers.run(input)

#textVar = ''

def find(input):
	textVar = ''
	response = helpers.run(input)
	textVar = 'Destination %s \n' % response['destination']
	for i in response['prices'].keys():
		textVar += '\tAirport: %s\n\tPrice: %f\n\tCarrier Name:%s\n' % (i, response['prices'][i]['Price'], response['prices'][i]['CarrierName'])
#	textentry.configure(text=textVar)
	return textVar

print find(input)

#top = Tkinter.Tk()

#quitButton = Tkinter.Button(top,text="Find Me A Holiday!",command=find(input))
#quitButton.grid(row=0, column=0)

#textentry = Tkinter.Entry(top, textvariable=textVar)
#textentry.grid(row=1, column=0)

#Tkinter.mainloop()

