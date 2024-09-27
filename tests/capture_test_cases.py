import builtins
import json
import os
import types

# Define the paths
CURRENT_DIR = os.path.dirname(__file__)
CAPTURED_TEST_CASES_FILE = os.path.join(CURRENT_DIR, 'captured_test_cases.json')

# List of data types to track
tracked_data_types = [
    bool,
    int,
    str,
    float,
    list,
    dict,
    # Custom classes will be handled dynamically, no need to list them here.
]

# Map data types to their corresponding key names
type_to_key = {
    bool: 'bools',
    int: 'ints',
    str: 'strings',
    float: 'floats',
    list: 'lists',
    dict: 'dicts',
    # Custom objects will have keys based on their class names
}

# Initialize test_case_data
test_case_data = {}

# Wrapping the input function to capture inputs and prompts
original_input = builtins.input
def input(prompt=""):
    global test_case_data
    # Capture the prompt
    test_case_data.setdefault("input_prompts", []).append(prompt)
    
    # Get actual user input
    user_input = original_input(prompt)
    
    # Log the input
    test_case_data.setdefault("inputs", []).append(user_input)
    
    return user_input

# Wrapping the print function to capture printed output
original_print = builtins.print
def print(*args, **kwargs):
    global test_case_data
    # Capture the printed messages
    message = " ".join(str(arg) for arg in args)
    test_case_data.setdefault("printed_messages", []).append(message)
    
    # Call the original print function
    original_print(*args, **kwargs)

# Function to safely serialize variables
def safe_serialize(value, variable_name, test_case_id):
    try:
        json.dumps(value)
        return value  # If serialization succeeds, return the value.
    except (TypeError, OverflowError, ValueError):
        # Serialize custom objects into dictionaries
        if hasattr(value, '__dict__'):
            return {
                '__class__': type(value).__name__,
                '__attributes__': value.__dict__
            }
        else:
            # For other non-serializable objects, return a string representation
            return repr(value)

# Function to capture global variables at the end of execution
def capture_global_variables(test_case_id, new_global_vars):
    global test_case_data
    for var_name, value in new_global_vars.items():
        if (
            var_name.startswith("__") or
            callable(value) or
            isinstance(value, types.ModuleType)
        ):
            continue
        serialized_value = safe_serialize(value, var_name, test_case_id)
        # Determine the type key for the variable
        for data_type in tracked_data_types:
            if isinstance(value, data_type):
                type_key = type_to_key.get(data_type, 'others')
                test_case_data.setdefault(type_key, {})[var_name] = serialized_value
                break
        else:
            # For custom objects, use their class name as the key
            if isinstance(serialized_value, dict) and '__class__' in serialized_value:
                class_name = serialized_value['__class__']
                test_case_data.setdefault(class_name, {})[var_name] = serialized_value
            else:
                # Store other types under 'others'
                test_case_data.setdefault('others', {})[var_name] = serialized_value

# Function to remove duplicates from lists while preserving order
def remove_duplicates(lst):
    seen = set()
    new_lst = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            new_lst.append(item)
    return new_lst

# Function to save the test case data to a JSON file
def save_test_case(test_cases):
    global test_case_data

    # Compute invalid_input_prompts and invalid_printed_messages
    all_input_prompts = set()
    all_printed_messages = set()
    for tc in test_cases:
        all_input_prompts.update(tc.get("input_prompts", []))
        all_printed_messages.update(tc.get("printed_messages", []))
    current_input_prompts = set(test_case_data.get("input_prompts", []))
    current_printed_messages = set(test_case_data.get("printed_messages", []))

    test_case_data["invalid_input_prompts"] = list(all_input_prompts - current_input_prompts)
    test_case_data["invalid_printed_messages"] = list(all_printed_messages - current_printed_messages)

    # Remove duplicates from lists
    test_case_data["input_prompts"] = remove_duplicates(test_case_data.get("input_prompts", []))
    test_case_data["inputs"] = remove_duplicates(test_case_data.get("inputs", []))
    test_case_data["printed_messages"] = remove_duplicates(test_case_data.get("printed_messages", []))
    test_case_data["invalid_input_prompts"] = remove_duplicates(test_case_data.get("invalid_input_prompts", []))
    test_case_data["invalid_printed_messages"] = remove_duplicates(test_case_data.get("invalid_printed_messages", []))

    # Build the ordered keys list dynamically
    ordered_keys = [
        "id_test_case",
        "test_case_description",
        "inputs",
        "input_prompts",
        "printed_messages",
    ]

    # Add keys for tracked data types
    for data_type in tracked_data_types:
        type_key = type_to_key.get(data_type, 'others')
        if type_key in test_case_data:
            ordered_keys.append(type_key)

    # Add keys for custom classes
    custom_class_keys = [key for key in test_case_data.keys() if key not in ordered_keys and key not in [
        'invalid_input_prompts', 'invalid_printed_messages', 'others']]
    ordered_keys.extend(custom_class_keys)

    # Always include 'others' if it exists
    if 'others' in test_case_data:
        ordered_keys.append('others')

    # Add invalid input prompts and printed messages
    ordered_keys.extend([
        "invalid_input_prompts",
        "invalid_printed_messages"
    ])

    # Reorder test_case_data based on ordered_keys
    ordered_test_case_data = {key: test_case_data[key] for key in ordered_keys if key in test_case_data}

    # Append the new test case
    test_cases.append(ordered_test_case_data)

    # Save back to the JSON file
    with open(CAPTURED_TEST_CASES_FILE, 'w') as f:
        json.dump(test_cases, f, indent=4)

# The main function to run the solution file and capture test case data
def run_and_capture(solution_file):
    global test_case_data
    # Re-initialize test_case_data
    test_case_data = {
        "id_test_case": None,
        "test_case_description": "",
        "inputs": [],
        "input_prompts": [],
        "printed_messages": [],
        "invalid_input_prompts": [],
        "invalid_printed_messages": []
    }

    # Initialize keys for the tracked data types
    for data_type in tracked_data_types:
        type_key = type_to_key.get(data_type, 'others')
        test_case_data[type_key] = {}

    # Inject our input/print hooks into the global namespace
    builtins.input = input
    builtins.print = print

    # Capture existing global variables before execution
    pre_existing_globals = set(globals().keys())

    # Run the solution file
    solution_path = os.path.abspath(os.path.join(CURRENT_DIR, '..', solution_file))
    with open(solution_path, 'r') as f:
        exec(f.read(), globals())

    # Identify new global variables introduced by the solution file
    new_global_vars = {k: v for k, v in globals().items() if k not in pre_existing_globals}

    # Load existing test cases to assign id_test_case
    if os.path.exists(CAPTURED_TEST_CASES_FILE):
        with open(CAPTURED_TEST_CASES_FILE, 'r') as f:
            test_cases = json.load(f)
    else:
        test_cases = []

    # Assign id_test_case
    if test_cases:
        last_id = max(tc.get("id_test_case", 0) for tc in test_cases)
    else:
        last_id = 0
    test_case_data["id_test_case"] = last_id + 1
    test_case_id = test_case_data["id_test_case"]

    # Capture global variables at the end
    capture_global_variables(test_case_id, new_global_vars)

    # Save the test case data to a JSON file
    save_test_case(test_cases)

    # Restore original input and print functions
    builtins.input = original_input
    builtins.print = original_print

if __name__ == '__main__':
    # Replace with the name of the file to collect test cases from
    run_and_capture("a4_solution_friend_tracker.py")