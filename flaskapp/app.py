#Flask app, searches CSV data from the web by various fields

from flask import Flask, render_template, request
import csv
import requests
from io import StringIO

app = Flask(__name__)

CSV_URL = "https://raw.githubusercontent.com/jinchen003/Nearabl.Sample.Data/main/us-500.csv"

def fetch_csv_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    selected_field = request.form.get('field')
    results = []

    csv_data = fetch_csv_data(CSV_URL)
    if csv_data:
        csv_reader = csv.DictReader(StringIO(csv_data, newline=''))
        for row in csv_reader:
            #combines the phone1 and phone2 fields into one search query
            if selected_field == 'phone_number':
                if query.lower() in row['phone1'].lower() or query.lower() in row['phone2'].lower() and row not in results:
                    results.append(row)
            #combines the address, city, state, county, and zip fields into one search query
            if selected_field == 'address':
                if query.lower() in row['address'].lower() or query.lower() in row['city'].lower() or query.lower() in row['state'].lower() or query.lower() in row['county'].lower() or query.lower() in row['zip'].lower() and row not in results:
                    results.append(row)
            if selected_field == 'all_columns':
                for key in row.keys():
                    if query.lower() in row[key].lower() and row not in results:
                        results.append(row)
                        break  
            elif query.lower() in row[selected_field].lower() and row not in results:
                results.append(row)
    return render_template("index.html", query = query, selected_field=selected_field, results = results)

if __name__ == '__main__':
    app.run()
