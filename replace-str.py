def replace_string_in_file(input_file_path, old_string, new_string, output_file_path):
    try:
        # Open the input file in read mode and read its contents
        with open(input_file_path, 'r') as file:
            file_contents = file.read()
        
        # Replace the target string with the new string
        updated_contents = file_contents.replace(old_string, new_string)
        
        # Open the output file in write mode and write the updated contents to the new file
        with open(output_file_path, 'w') as file:
            file.write(updated_contents)
        
        print(f"Successfully replaced '{old_string}' with '{new_string}' and saved to {output_file_path}")
    except FileNotFoundError:
        print(f"Error: The file {input_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
replace_string_in_file('trfmvmtst.txt', '"name-replaceme"', '"vmname"', 'output.txt')
