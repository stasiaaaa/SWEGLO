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

if __name__ == '__main__':
    app.run(debug=True)