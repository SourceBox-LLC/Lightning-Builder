from flask import Flask, request, jsonify, render_template, send_file, session
from flask_cors import CORS
import yaml
import os
import random
import shutil
from build import gather_templates, compile_templates, gpt_rewrite, export_final_template, generate_requirements
import logging
import zipfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
CORS(app)  # Enable CORS if needed

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/build')
def build():
    return render_template('build.html')

@app.route('/generate-config', methods=['POST'])
def generate_config():
    data = request.json
    logger.info(f"Received data for configuration generation: {data}")

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

    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, 'build-config.yaml')

    try:
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)
        logger.info(f"Configuration file created at: {config_file_path}")
        session['config_file_path'] = config_file_path  # Store in session
    except Exception as e:
        logger.error(f"Error writing configuration file: {e}")
        return jsonify({'error': 'Failed to write configuration file.'}), 500

    return jsonify({
        'message': 'Configuration file generated successfully',
        'config_file_path': config_file_path
    })



@app.route('/custom-config', methods=['POST'])
def custom_config():
    data = request.json
    logger.info("Received request for custom configuration.")
    
    config_content = data.get('config')
    logger.debug(f"Config content received: {config_content}")

    if not config_content:
        logger.error("No configuration content provided.")
        return jsonify({'error': 'No configuration content provided.'}), 400

    try:
        # Parse the YAML configuration content
        config_data = yaml.safe_load(config_content)
        logger.info(f"Parsed configuration data: {config_data}")

        # Write the configuration to a file
        cwd = os.getcwd()
        config_file_path = os.path.join(cwd, 'build-config.yaml')
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)
        logger.info(f"Custom configuration file created at: {config_file_path}")

        # Store the configuration data in the session
        session['config_data'] = config_data
        session['config_file_path'] = config_file_path
        logger.info("Configuration data stored in session.")

        return jsonify({
            'message': 'Custom configuration processed successfully',
            'config_file_path': config_file_path,
            'config_data': config_data
        })
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        return jsonify({'error': 'Failed to parse configuration file.'}), 500
    except Exception as e:
        logger.error(f"Error writing custom configuration file: {e}")
        return jsonify({'error': 'Failed to write custom configuration file.'}), 500



@app.route('/display-config')
def display_config():
    logger.info("Received request to display configuration.")
    
    config_file_path = session.get('config_file_path')
    logger.debug(f"Config file path from session: {config_file_path}")

    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    logger.info("Returning configuration data as JSON.")
    return jsonify(config_data)

@app.route('/assemble-config', methods=['POST'])
def assemble_config():
    config_file_path = session.get('config_file_path')  # Get from session

    if config_file_path is None or not os.path.exists(config_file_path):
        logger.error("Configuration file not found.")
        return jsonify({'error': 'Configuration file not found.'}), 400

    logger.info(f"Reading configuration from: {config_file_path}")

    try:
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            logger.info("Configuration data successfully loaded.")
    except Exception as e:
        logger.error(f"Error reading configuration file: {e}")
        return jsonify({'error': 'Failed to read configuration file.'}), 500

    try:
        logger.info("Gathering templates based on the configuration.")
        templates = gather_templates(config_data)

        logger.info("Compiling templates into a single string.")
        compiled_template = compile_templates(templates)

        logger.info("Rewriting the compiled template using GPT.")
        final_template = gpt_rewrite(compiled_template)

        logger.info("Generating requirements based on the final template.")
        requirements = generate_requirements(final_template, config_file_path)

        logger.info("Exporting the final template and requirements to the current working directory.")
        output_dir, template_file_path, requirements_file_path, build_file_destination_path = export_final_template(final_template, config_file_path)

        # Write the requirements to the file
        with open(requirements_file_path, 'w') as req_file:
            req_file.write(requirements)

        # Store the paths in the session
        session['template_file_path'] = template_file_path
        session['requirements_file_path'] = requirements_file_path
        session['build_file_destination_path'] = build_file_destination_path

        logger.info(f"Template file path: {template_file_path}")
        logger.info(f"Requirements file path: {requirements_file_path}")
        logger.info(f"Build file path: {build_file_destination_path}")

        logger.info("Template assembled successfully.")
    except Exception as e:
        logger.error(f"Error during template assembly: {e}")
        return jsonify({'error': 'Failed to assemble template.'}), 500

    return jsonify({
        'message': 'Template assembled successfully',
        'file_path': template_file_path,
        'requirements_path': requirements_file_path,
        'build_file_path': build_file_destination_path,
        'final_template': final_template,
        'requirements': requirements
    })

@app.route('/download-agent', methods=['POST'])
def download_agent():
    # Retrieve paths from the session
    template_file_path = session.get('template_file_path')
    requirements_file_path = session.get('requirements_file_path')
    build_file_destination_path = session.get('build_file_destination_path')

    logger.debug(f"Attempting to download files with paths: {template_file_path}, {requirements_file_path}, {build_file_destination_path}")

    # Check if any file path is missing from the session
    if not all([template_file_path, requirements_file_path, build_file_destination_path]):
        logger.error("One or more file paths are missing from the session.")
        return jsonify({'error': 'File paths are missing.'}), 400

    # Check if each file exists and log if any are missing
    missing_files = []
    for path, name in zip(
        [template_file_path, requirements_file_path, build_file_destination_path],
        ['Template file', 'Requirements file', 'Build file']
    ):
        if not os.path.exists(path):
            missing_files.append(name)
            logger.error(f"{name} not found at path: {path}")

    if missing_files:
        return jsonify({'error': f"Files not found: {', '.join(missing_files)}"}), 400

    # Create the archive directory if it doesn't exist
    archive_dir = os.path.join(os.getcwd(), 'archive')
    os.makedirs(archive_dir, exist_ok=True)

    zip_file_name = f"agent_template_{random.randint(10000, 99999)}.zip"
    zip_file_path = os.path.join(archive_dir, zip_file_name)
    logger.info(f"Creating zip file: {zip_file_path}")

    try:
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file_path in [template_file_path, requirements_file_path, build_file_destination_path]:
                logger.debug(f"Adding file to zip: {file_path}")
                zipf.write(file_path, arcname=os.path.basename(file_path))
        
        logger.info(f"Successfully created zip file: {zip_file_path}")

        # Send the zip file to the user
        return send_file(zip_file_path, as_attachment=True, download_name=zip_file_name)

    except Exception as e:
        logger.error(f"Error while creating or sending the zip file: {e}")
        return jsonify({'error': 'Failed to create or send the zip file.'}), 500




@app.route('/delete-files', methods=['POST'])
def delete_files():
    # Retrieve paths from the session
    template_file_path = session.get('template_file_path')
    requirements_file_path = session.get('requirements_file_path')
    build_file_destination_path = session.get('build_file_destination_path')
    zip_file_path = session.get('zip_file_path')

    # Determine the directory to delete
    if template_file_path:
        agent_dir = os.path.dirname(template_file_path)
    else:
        logger.error("Template file path is missing.")
        return jsonify({'error': 'Template file path is missing.'}), 400

    # Delete the zip file
    if zip_file_path and os.path.exists(zip_file_path):
        try:
            os.remove(zip_file_path)
            logger.info(f"Deleted zip file: {zip_file_path}")
        except Exception as e:
            logger.error(f"Error deleting zip file {zip_file_path}: {e}")
            return jsonify({'error': 'Failed to delete zip file.'}), 500

    # Delete the agent template directory
    if os.path.exists(agent_dir):
        try:
            shutil.rmtree(agent_dir)
            logger.info(f"Deleted agent directory: {agent_dir}")
        except Exception as e:
            logger.error(f"Error deleting agent directory {agent_dir}: {e}")
            return jsonify({'error': 'Failed to delete agent directory.'}), 500

    return jsonify({'message': 'Files and directory deleted successfully.'})




@app.route('/upload-config', methods=['POST'])
def upload_config():
    data = request.json
    config_content = data.get('config')

    if not config_content:
        return jsonify({'error': 'No configuration content provided.'}), 400

    config_file_path = os.path.join(os.getcwd(), 'build-config.yaml')

    try:
        with open(config_file_path, 'w') as file:
            file.write(config_content)
        logger.info(f"Custom configuration file uploaded at: {config_file_path}")
        session['config_file_path'] = config_file_path  # Store in session
    except Exception as e:
        logger.error(f"Error writing custom configuration file: {e}")
        return jsonify({'error': 'Failed to write custom configuration file.'}), 500

    return jsonify({'message': 'Custom configuration uploaded successfully'})





if __name__ == '__main__':
    app.run(debug=True)
