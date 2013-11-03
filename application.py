from flask import Flask, render_template, redirect,request
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
  dc = request.form.get("depart-country")
  return "hi"

if __name__ == '__main__':
    app.run(debug=True)
