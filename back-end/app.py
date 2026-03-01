from flask import Flask, jsonify
from flask_cors import CORS
import json
import requests
app = Flask(__name__)
CORS(app)

#Parameterized API endpoint
@app.route('/api/relations/<country_name>', methods=['GET'])
def get_relations(country_name):
    with open('data/relations.json') as f:
        data = json.load(f)
    
    match = next((r for r in data if r['country'].lower() == country_name.lower()), None)
    
    if match:
        return jsonify(match)
    else:
        return jsonify({'error': 'No data found'}), 404


@app.route('/api/nato', methods=['GET'])
def get_nato_members():
    with open('data/nato_members.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/nato/<country_name>', methods=['GET'])
def get_nato_member(country_name):
    with open('data/nato_members.json') as f:
        data = json.load(f)
    
    match = next((r for r in data if r['country'].lower() == country_name.lower()), None)
    
    if match:
        return jsonify({'nato_member': True})
    else:
        return jsonify({'nato_member': False})


@app.route('/api/military/<country_code>', methods=['GET'])
def get_military(country_code):
    url = f'https://api.worldbank.org/v2/country/{country_code}/indicator/MS.MIL.XPND.GD.ZS?format=json&mrv=1'
    
    response = requests.get(url)
    raw = response.json()
    
    try:
        value = raw[1][0]['value']
        country = raw[1][0]['country']['value']
        year = raw[1][0]['date']
        return jsonify({
            'country': country,
            'indicator': 'Military expenditure % of GDP',
            'value': value,
            'year': year,
            'source': 'World Bank'
        })
    except (IndexError, KeyError, TypeError):
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(debug=True)