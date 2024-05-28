def replace_string_in_file(input_file_path, output_file_path, old_string, new_string):
    try:
        # Read the contents of the input file
        with open(input_file_path, 'r') as file:
            file_data = file.read()

        # Replace the old string with the new string
        new_data = file_data.replace(old_string, new_string)

        # Write the new data to the output file
        with open(output_file_path, 'w') as file:
            file.write(new_data)

        print(f"Replaced '{old_string}' with '{new_string}' and saved to '{output_file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file = 'smpl.txt'
output_file = 'modified_smpl.txt'
replace_string_in_file(input_file, output_file, 'old_string', 'new_string')
