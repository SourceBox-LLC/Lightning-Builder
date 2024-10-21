from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import yaml
import tempfile
import os, shutil, random
from build import gather_templates, compile_templates, gpt_rewrite, export_final_template, generate_requirements
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    # Log the incoming request data
    data = request.json
    logger.info(f"Received data for configuration generation: {data}")

    # Prepare the configuration data
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
    logger.info(f"Temporary directory created at: {temp_dir}")

    # Define the path for the build-config.yaml file
    config_file_path = os.path.join(temp_dir, 'build-config.yaml')

    # Write the configuration to the YAML file in the temporary directory
    try:
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)
        logger.info(f"Configuration file created at: {config_file_path}")
    except Exception as e:
        logger.error(f"Error writing configuration file: {e}")
        return jsonify({'error': 'Failed to write configuration file.'}), 500

    return jsonify({
        'message': 'Configuration file generated successfully',
        'config_file_path': config_file_path  # Optionally return the path
    })



@app.route('/display-config')
def display_config():
    global config_file_path  # Use the global variable to access the configuration file path

    # Check if the configuration file path is valid
    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    # Read the configuration from the YAML file
    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    logger.info("Returning configuration data as JSON.")
    return jsonify(config_data)  # Return the configuration data as JSON



@app.route('/assemble-config', methods=['POST'])
def assemble_config():
    global config_file_path  # Use the global variable to access the configuration file path

    # Check if the configuration file path is valid
    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    # Read the configuration from the YAML file
    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    # Gather templates based on the configuration
    logger.info("Gathering templates based on the configuration.")
    templates = gather_templates(config_data)

    # Compile the templates into one string
    logger.info("Compiling templates into a single string.")
    compiled_template = compile_templates(templates)

    # Rewrite the compiled template using GPT
    logger.info("Rewriting the compiled template using GPT.")
    final_template = gpt_rewrite(compiled_template)

    # Generate requirements using the final template
    logger.info("Generating requirements based on the final template.")
    requirements = generate_requirements(final_template, config_file_path)  # Pass the build file path

    # Export the final template to a folder and get all paths
    logger.info("Exporting the final template and requirements to the temporary directory.")
    temp_dir, template_file_path, requirements_file_path, build_file_destination_path = export_final_template(final_template, config_file_path)

    logger.info("Template assembled successfully.")
    return jsonify({
        'message': 'Template assembled successfully',
        'file_path': template_file_path,  # Path to the template file
        'requirements_path': requirements_file_path,  # Path to the requirements file
        'build_file_path': build_file_destination_path,  # Path to the build file
        'final_template': final_template,
        'requirements': requirements  # Include requirements in the response
    })





@app.route('/download-agent', methods=['POST'])
def download_agent():
    global config_file_path  # Use the global variable to access the configuration file path

    # Check if the configuration file path is valid
    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    # Define the temporary directory where the files are stored
    temp_dir = os.path.dirname(config_file_path)  # Get the directory of the config file
    logger.info(f"Temporary directory for download: {temp_dir}")

    # Create a zip file name
    zip_file_name = f"agent_template_{random.randint(10000, 99999)}.zip"
    zip_file_path = os.path.join(temp_dir, zip_file_name)
    logger.info(f"Creating zip file: {zip_file_path}")

    try:
        # Zip the directory
        shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', temp_dir)
        logger.info(f"Successfully created zip file: {zip_file_path}")

        # Send the zip file to the user
        return send_file(zip_file_path, as_attachment=True)

    except Exception as e:
        logger.error(f"Error while creating or sending the zip file: {e}")
        return jsonify({'error': 'Failed to create or send the zip file.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
