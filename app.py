from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yaml

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# In-memory storage for demonstration purposes
flowchart_data = {}

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/build')
def build():
    return render_template('build.html')

@app.route('/generate-config', methods=['POST'])
def generate_config():
    data = request.json
    config = {
        'project': {
            'name': 'LightningBuilderApp',
            'version': '1.0.0',
            'description': 'Configuration for building the Lightning Builder app'
        },
        'build': {
            'model': data.get('selected_model'),
            'toolkits': data.get('selected_toolkits', []),
            'prompt': data.get('agent_prompt')
        }
    }
    
    with open('build-config.yaml', 'w') as file:
        yaml.dump(config, file)
    
    return jsonify({'message': 'Configuration file generated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
