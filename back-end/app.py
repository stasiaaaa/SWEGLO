from flask import Flask, jsonify
from flask_cors import CORS
import json

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
def get_is_nato_member(country_name):
    with open('data/nato_members.json') as f:
        data = json.load(f)
    
    match = next((r for r in data if r["country"].lower() == country_name.lower()), None)

    if match:
        return jsonify(match)
    return jsonify({'nato_member': 'No'}) # TODO: countryname from input

if __name__ == '__main__':
    app.run(debug=True)