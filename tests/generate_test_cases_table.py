import json
import os

# Path to the project folder's `tests/` directory
tests_folder = "tests"

# Path to the input JSON file
json_file_path = os.path.join(tests_folder, "test_cases_final.json")

# Path to the output HTML file
output_file_path = os.path.join(tests_folder, "test_cases_table_output.html")

# Specify the keys you want to include in the output columns
keys_to_include = ['dicts']  # You can add other keys like 'bools', 'strings', 'lists', etc.

# Load the JSON data from the file
with open(json_file_path, "r") as file:
    json_data = json.load(file)

# HTML structure
html = """<table border="1">
    <thead>
        <tr>
            <th>Description</th>
            <th>Input</th>"""

# Add headers dynamically based on keys_to_include
for key in keys_to_include:
    html += f"<th>Expected Output: {key}</th>"

html += """</tr>
    </thead>
    <tbody>"""  # This line has been fixed to avoid adding extra newlines.

# Function to simplify the dictionary by ignoring the outer key and only returning the inner value
def simplify_dict(d):
    if isinstance(d, dict) and len(d) == 1 and isinstance(next(iter(d.values())), dict):
        return next(iter(d.values()))  # Return only the inner dictionary
    return d  # Return the original if it's not a dict of dicts

# Loop through each test case and generate rows
for test_case in json_data:
    description = f"{test_case['id_test_case']}. {test_case['test_case_description']}"
    inputs = ", ".join(f'"{inp}"' for inp in test_case['inputs'])
    
    html += f"""<tr>
            <td>{description}</td>
            <td><code>{inputs}</code></td>"""
    
    # Add the values for each specified key
    for key in keys_to_include:
        value = test_case.get(key, {})
        
        # Only extract the inner values of the dictionaries
        simplified_value = {}
        for inner_key, inner_value in value.items():
            simplified_value = inner_value if isinstance(inner_value, dict) else {inner_key: inner_value}
        
        html += f"<td><code>{json.dumps(simplified_value)}</code></td>"
    
    html += "</tr>"

html += """</tbody>
</table>"""

# Output the HTML content to the tests/ folder
with open(output_file_path, "w") as file:
    file.write(html)

print(f"HTML file generated: {output_file_path}")