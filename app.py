import functions
from flask import Flask, render_template, request
import urllib.parse, urllib.request, urllib.error, json
import pprint
from keys import api_key1

# Create an instance of Flask
app = Flask(__name__)

@app.route('/')
def home():
    try:
        data = functions.get_city_data()
        print("DEBUG: Data returned by get_city_data:", data)
        return render_template("index.html", data=data)
    except Exception as e:
        print(f"Error in home route: {e}")
        return "An error occurred while processing your request.", 500

@app.route('/search')
def search():
    query = request.args.get('query', '')
    # Filter data based on the query (example logic below)
    filtered_data = [item for item in data if query.lower() in item['city'].lower()]
    return render_template('results.html', data=filtered_data)

if __name__ == "__main__":
    app.run(debug=True)
