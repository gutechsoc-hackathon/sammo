from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")
@app.route('/css/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	return redirect("/static/"+path)

if __name__ == '__main__':
    app.run(debug = True, port = 80)


