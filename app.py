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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Get the search query
    # data = functions.get_city_data(query)
    # return render_template("result.html", data=data)
    print(f"DEBUG: Received search query: {query}")  # Log the query
    if not query:
        return render_template('results.html', error="Please enter a city name.")

    try:
        data = functions.get_city_data(query)
        print(f"DEBUG: Data returned by get_city_data: {data}")
        if not data:
            return render_template('results.html', error=f"No data found for city: {query}")

        return render_template('results.html', data=data)

    except Exception as error:
        # Catch any unexpected errors and log them
        print(f"ERROR in search route: {error}")
        return render_template('results.html', error="An error occurred while processing your request.")

if __name__ == "__main__":
    app.run(debug=True, port=5001)