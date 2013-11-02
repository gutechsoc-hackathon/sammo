from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	if request.method == 'POST':

    return 	'''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

if __name__ == '__main__':
    app.run()

def createSession(apikey, country, currency, locale, originPlace, destinationPlace, outboundDate,
					inboundDate = "", locationSchema = "", cabinClass = "", adults = "", children = "", infants = ""):
