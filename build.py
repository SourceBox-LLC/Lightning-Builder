import tempfile
import os

def create_temp_directory():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created at: {temp_dir}")

    # Perform operations within the temporary directory
    # For example, create a temporary file
    temp_file_path = os.path.join(temp_dir, 'temp_file.txt')
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("This is a temporary file.")

    print(f"Temporary file created at: {temp_file_path}")

    # Return the path of the temporary directory
    return temp_dir

# Example usage
if __name__ == "__main__":
    temp_directory = create_temp_directory()
    # Do something with the temporary directory
    # Note: The directory will not be automatically deleted