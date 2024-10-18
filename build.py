import tempfile
import os
import yaml

def create_temp_directory():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    # Define the path for the build-config.yaml file
    config_file_path = os.path.join(temp_dir, 'build-config.yaml')

    # Example configuration data
    config = {
        'project': {
            'name': 'ExampleProject',
            'version': '1.0.0',
            'description': 'Example configuration for a project'
        },
        'build': {
            'model': 'ExampleModel',
            'toolkits': ['Toolkit1', 'Toolkit2'],
            'prompt': 'This is an example prompt.'
        }
    }

    # Write the configuration to the YAML file
    with open(config_file_path, 'w') as file:
        yaml.dump(config, file)

    print(f"Configuration file created at: {config_file_path}")

    return config_file_path

def read_config_file(config_file_path):
    # Check if the file exists
    if not os.path.exists(config_file_path):
        print("Configuration file not found.")
        return None

    # Read the configuration from the YAML file
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)

    print("Configuration read from file:")
    print(config)
    return config


def build_from_config(config_file_path):

# Example usage
if __name__ == "__main__":
    config_file_path = create_temp_directory()
    config = read_config_file(config_file_path)
