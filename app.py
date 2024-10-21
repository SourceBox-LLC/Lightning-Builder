from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yaml
import tempfile
import os
from build import gather_templates, compile_templates, gpt_rewrite, export_final_template  # Import the necessary functions

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# In-memory storage for demonstration purposes
flowchart_data = {}
config_file_path = None  # Global variable to store the configuration file path

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/build')
def build():
    return render_template('build.html')

@app.route('/generate-config', methods=['POST'])
def generate_config():
    global config_file_path  # Use the global variable to store the configuration file path
    data = request.json
    config_data = {
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
        yaml.dump(config_data, file)
    
    print(f"Configuration file created at: {config_file_path}")
    
    return jsonify({
        'message': 'Configuration file generated successfully',
        'config_file_path': config_file_path  # Optionally return the path
    })



@app.route('/display-config')
def display_config():
    global config_file_path  # Use the global variable to access the configuration file path

    if config_file_path is None or not os.path.exists(config_file_path):
        return jsonify({'error': 'Configuration file not found.'}), 400

    # Read the configuration from the YAML file
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    return jsonify(config_data)  # Return the configuration data as JSON



@app.route('/assemble-config', methods=['POST'])
def assemble_config():
    global config_file_path  # Use the global variable to access the configuration file path

    if config_file_path is None or not os.path.exists(config_file_path):
        return jsonify({'error': 'Configuration file not found.'}), 400

    # Read the configuration from the YAML file
    with open(config_file_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Gather templates based on the configuration
    templates = gather_templates(config_data)
    
    # Compile the templates into one string
    compiled_template = compile_templates(templates)
    
    # Rewrite the compiled template using GPT
    final_template = gpt_rewrite(compiled_template)
    
    # Export the final template to a file
    file_path, file_name = export_final_template(final_template)
    
    return jsonify({
        'message': 'Template assembled successfully',
        'file_path': file_path,
        'file_name': file_name,
        'final_template': final_template  # Include the final template in the response
    })



if __name__ == '__main__':
    app.run(debug=True)
