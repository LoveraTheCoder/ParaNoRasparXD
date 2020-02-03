from flask import Flask, render_template # Primero importamos el módulo

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/links')
def links():
  return render_template('links.html')

@app.route('/sitios')
def sitios():
  return render_template('sitios.html')

if __name__ == '__main__':
	app.run(debug=True)