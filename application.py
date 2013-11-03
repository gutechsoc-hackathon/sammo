from flask import Flask, render_template, redirect,request
import helpers
app = Flask(__name__, static_url_path ='/static')

@app.route('/')
def index():	
	return render_template('index.html')

@app.route('/<path:path>')
def catch_all(path):
        if path.startswith("css/") or path.startswith("js/"):
            return redirect("/static/"+path)


@app.route('/get_flight_data', methods=['POST'])
def flight_data():
  da = request.form.get("depart-airport")
  dc = request.form.get("depart-country")
  dd = request.form.get("depart-date")
  ac = request.form.get("arrive-country")
  input = {'countryTo': ac, 'leavingAirport': da, 'departDate': dd}
  return "helpers.run(input)"

if __name__ == '__main__':
    app.run(debug=True)
