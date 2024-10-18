from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yaml
import tempfile
import os

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
            'name': data.get('agent_name'),
            'version': '1.0.0',
            'description': data.get('agent_description')
        },
        'build': {
            'model': data.get('selected_model'),
            'toolkits': data.get('selected_toolkits', []),
            'prompt': data.get('agent_prompt')
        }
    }
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    # Define the path for the build-config.yaml file
    config_file_path = os.path.join(temp_dir, 'build-config.yaml')
    
    # Write the configuration to the YAML file in the temporary directory
    with open(config_file_path, 'w') as file:
        yaml.dump(config, file)
    
    print(f"Configuration file created at: {config_file_path}")
    
    return jsonify({
        'message': 'Configuration file generated successfully',
        'config_file_path': config_file_path  # Optionally return the path
    })

if __name__ == '__main__':
    app.run(debug=True)
