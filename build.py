import tempfile
import os
import yaml
from openai import OpenAI
from dotenv import load_dotenv
import random



load_dotenv()

client = OpenAI()



def test_config():

    def create_temp_directory():
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Define the path for the build-config.yaml file
        config_file_path = os.path.join(temp_dir, 'build-config.yaml')

        # Example configuration data
        config = {
            'project': {
                'name': 'Search Assistant',
                'version': '1.0.0',
                'description': 'a search agent with access to wikipedia and the duckduckgo engine.'
            },
            'build': {
                'model': 'Anthropic',
                'toolkits': ['Duck Duck Go Search', 'Wikipedia Search'],
                'prompt': 'You are a helpful search assistant.'
            }
        }

        # Write the configuration to the YAML file
        with open(config_file_path, 'w') as file:
            yaml.dump(config, file)

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
    
    config_file_path = create_temp_directory()
    config = read_config_file(config_file_path)
    return config





def gather_templates(config):

    # Read the configuration from the YAML file
    template_dict = {}

    start_template_path = os.path.join('lightning-plates', 'start template', 'start.txt')

    # Attempt to read the content of the start.txt file
    try:
        with open(start_template_path, 'r') as file:
            start_template = file.read()
        
    except FileNotFoundError:
        print(f"Error: The file '{start_template_path}' was not found.")
        return  # Exit the function if the file is not found

    template_dict["start"] = start_template
    
    # Check if the model is 'Anthropic'
    if config['build']['model'] == 'Anthropic':
        # Define the path for the anthropic.txt file
        anthropic_file_path = os.path.join('lightning-plates', 'main template', 'models', 'anthropic.txt')
        
        # Read the content of the anthropic.txt file
        with open(anthropic_file_path, 'r') as file:
            anthropic_content = file.read()

        model_template = anthropic_content

        template_dict["model template"] = model_template




    # check which tools are being used
    toolkits = config['build']['toolkits']

    tool_templates_list = []

    for tool in toolkits:
        if tool == 'Duck Duck Go Search':
            duckduckgo_search_path = os.path.join('lightning-plates', 'main template', 'tools', 'duckduckgo_search.txt')

            # Read the content of the anthropic.txt file
            with open(duckduckgo_search_path, 'r') as file:
                duckduckgo_search_tool = file.read()
            

            tool_templates_list.append(duckduckgo_search_tool)

        elif tool == 'Wikipedia Search':
            wikipedia_search_path = os.path.join('lightning-plates', 'main template', 'tools', 'wikipedia_search.txt')

            # Read the content of the anthropic.txt file
            with open(wikipedia_search_path, 'r') as file:
                wikipedia_search_tool = file.read()

            tool_templates_list.append(wikipedia_search_tool)

        else:
            print('Error: no tools found')
    

    template_dict["toolkits"] = tool_templates_list

    #add end template
    end_template_path = os.path.join('lightning-plates', 'end template', 'end.txt')

    # Read the content of the anthropic.txt file
    with open(end_template_path, 'r') as file:
        end_template = file.read()

    template_dict["end"] = end_template

    return template_dict





# compile templates into one
def compile_templates(templates):
    # Initialize an empty string to hold the compiled templates
    compiled_template = ""

    # Iterate through the templates in the dictionary and concatenate them
    for key, value in templates.items():
        if isinstance(value, list):  # Check if the value is a list (like toolkits)
            for item in value:
                compiled_template += f"{item}\n\n"  # Add each item followed by two newlines for separation
        else:
            compiled_template += f"{value}\n\n"  # Add each template followed by two newlines for separation

    return compiled_template  # Return the compiled string


        
def gpt_rewrite(compiled_template):
    try:
        # Call GPT API with formatted history and vector results
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''
                You are a template compiler and expert programmer.
                You are to take the template pieces you are given and re format them to create one final template.

                RULES:
                - no redundency or errors.
                - write out the full entire script.
                - all imports go at the top.
                - tools go together
                '''},
                {"role": "user", "content": compiled_template}
            ]
        )

        response_content = response.choices[0].message.content
        return response_content

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return f"Error: {e}"


def export_final_template(final_template):

    # Generate a random 5 digit number
    random_number = random.randint(10000, 99999)
    print(f"Generated random 5 digit number: {random_number}")

    # Create a temporary directory if it doesn't exist
    temp_dir = tempfile.gettempdir()  # Get the path to the temporary directory
    file_name = f'user_template_{random_number}.py'
    file_path = os.path.join(temp_dir, file_name)  # Define the path for the new file

    # Open the file in append mode and write the final_template to it
    with open(file_path, 'a') as file:  # 'a' mode to append to the file
        file.write(final_template)  # Write the final_template content to the file

    print(f"file name: {file_name}")
    print(f"Final template exported to: {file_path}")  # Optional: Print the file path for confirmation

    return file_path, file_name



# Example usage
if __name__ == "__main__":
    
    config_file = test_config()
    templates = gather_templates(config_file)

    print("\n\nCOMPILED TEMPLATE:\n\n")
    compiled_template = compile_templates(templates)
    print(compiled_template)


    print("\n\nFINAL TEMPLATE:\n\n")
    final_template = gpt_rewrite(compiled_template)
    print(final_template)


    print("\n\nExporting Template.........\n\n")
    export_final_template(final_template)

