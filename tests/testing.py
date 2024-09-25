import pandas as pd

# Function to lookup the actual values based on IDs
def get_values_from_ids(ids_str, lookup_df, id_col, value_col):
    # Ensure we are working with strings, since everything was loaded as strings
    ids = [i.strip() for i in ids_str.split(',')]  # Strip spaces and keep as strings
    values = lookup_df[lookup_df[id_col].isin(ids)][value_col].tolist()  # Find matching rows and return the values
    return values
test_cases_excel_path = r"tests/test_cases.xlsx"

"""
Loads in test cases from the test_cases.xlsx file
test_cases.xlsx is (sort of) designed to be normalized, so after
importing each
The dataframe it returns will have columns for:
    'id_test_case' (int),
    'test_description' (str),
    'input_ids' (str or int),
    'expected_input_prompt_ids' (str or int),
    'expected_printed_message_ids'(str or int),
    'expected_dictionaries_ids' (str or int),
    'input_values' (list),
    'expected_input_prompt_values' (list),
    'expected_printed_message_values' (list),
    'expected_dictionaries_values' (list), 
    'invalid_input_prompt_values' (list),
    'invalid_printed_message_values' (list)
"""
# Load the Excel file and read all sheets into a dictionary
# Load individual sheets from the Excel file, ensuring all columns are loaded as strings
test_cases_df = pd.read_excel(test_cases_excel_path, sheet_name='test_cases', dtype=str)
inputs_df = pd.read_excel(test_cases_excel_path, sheet_name='inputs', dtype=str)
input_prompts_df = pd.read_excel(test_cases_excel_path, sheet_name='input_prompts', dtype=str)
printed_messages_df = pd.read_excel(test_cases_excel_path, sheet_name='printed_messages', dtype=str)
dictionaries_df = pd.read_excel(test_cases_excel_path, sheet_name='dictionaries', dtype=str)

# Expand the test_cases_df with the actual values from the individual sheets
# input values
test_cases_df['input_values'] = test_cases_df['input_ids'].apply(
    lambda x: get_values_from_ids(x, inputs_df, 'id_input', 'input')
)
# input_prompt values
test_cases_df['expected_input_prompt_values'] = test_cases_df['expected_input_prompt_ids'].apply(
    lambda x: get_values_from_ids(x, input_prompts_df, 'id_input_prompt', 'input_prompt')
)
# printed message values
test_cases_df['expected_printed_message_values'] = test_cases_df['expected_printed_message_ids'].apply(
    lambda x: get_values_from_ids(x, printed_messages_df, 'id_printed_message', 'printed_message')
)
# dictionary values
test_cases_df['expected_dictionaries_values'] = test_cases_df['expected_dictionaries_ids'].apply(
    lambda x: get_values_from_ids(x, dictionaries_df, 'id_dictionary', 'dictionary')
)

# Add invalid_input_prompt_values: those in input_prompts_df that aren't in expected_input_prompt_values
all_input_prompts = input_prompts_df['input_prompt'].tolist()

test_cases_df['invalid_input_prompt_values'] = test_cases_df['expected_input_prompt_values'].apply(
    lambda valid_prompts: [prompt for prompt in all_input_prompts if prompt not in valid_prompts]
)

# Add invalid_printed_message_values: those in printed_messages_df that aren't in expected_printed_message_values
all_printed_messages = printed_messages_df['printed_message'].tolist()

test_cases_df['invalid_printed_message_values'] = test_cases_df['expected_printed_message_values'].apply(
    lambda valid_messages: [message for message in all_printed_messages if message not in valid_messages]
)

import pandas as pd

# Set options to display all rows and columns
pd.set_option('display.max_rows', None)        # Display all rows
pd.set_option('display.max_columns', None)     # Display all columns
pd.set_option('display.max_colwidth', None)    # Display full column content

print(test_cases_df)





# # Function to lookup the actual values based on IDs
# def get_values_from_ids(ids_str, lookup_df, id_col, value_col):
#     if not isinstance(ids_str, str):
#         ids_str = str(ids_str)
#     ids = [int(i) for i in ids_str.split(',')]  # Convert the comma-separated string into a list of integers
#     values = lookup_df[lookup_df[id_col].isin(ids)][value_col].tolist()  # Find matching rows and return the values
#     return values

# # Load the Excel file and read all sheets into a dictionary
# file_path = 'tests/a4_test_cases.xlsx'
# sheets_dict = pd.read_excel(file_path, sheet_name=None)

# # Access individual DataFrames
# test_cases_df = sheets_dict['test_cases']
# inputs_df = sheets_dict['inputs']
# input_prompts_df = sheets_dict['input_prompts']
# printed_messages_df = sheets_dict['printed_messages']
# dictionaries_df = sheets_dict['dictionaries']

# #print(test_cases_df)

# # Expand the test_cases_df with the actual values from the individual sheets
# # input values
# test_cases_df['input_values'] = test_cases_df['input_ids'].apply(
#     lambda x: get_values_from_ids(x, inputs_df, 'id_input', 'input')
# )
# # input_prompt values
# test_cases_df['expected_input_prompt_values'] = test_cases_df['expected_input_prompt_ids'].apply(
#     lambda x: get_values_from_ids(x, input_prompts_df, 'id_input_prompt', 'input_prompt')
# )
# # printed message values
# test_cases_df['expected_printed_message_values'] = test_cases_df['expected_printed_message_ids'].apply(
#     lambda x: get_values_from_ids(x, printed_messages_df, 'id_printed_message', 'printed_message')
# )
# # printed message values
# test_cases_df['expected_dictionaries_values'] = test_cases_df['expected_dictionaries_ids'].apply(
#     lambda x: get_values_from_ids(x, dictionaries_df, 'id_dictionary', 'dictionary')
# )

# # Add invalid_input_prompt_values: those in input_prompts_df that aren't in expected_input_prompt_values
# all_input_prompts = input_prompts_df['input_prompt'].tolist()

# test_cases_df['invalid_input_prompt_values'] = test_cases_df['expected_input_prompt_values'].apply(
#     lambda valid_prompts: [prompt for prompt in all_input_prompts if prompt not in valid_prompts]
# )

# # Add invalid_printed_message_values: those in printed_messages_df that aren't in expected_printed_message_values
# all_printed_messages = printed_messages_df['printed_message'].tolist()

# test_cases_df['invalid_printed_message_values'] = test_cases_df['expected_printed_message_values'].apply(
#     lambda valid_messages: [message for message in all_printed_messages if message not in valid_messages]
# )

# # Now test_cases_df contains the expanded inputs and printed messages

# print(test_cases_df['expected_printed_message_values'].tolist())
# print("\n\n")
# print(test_cases_df['invalid_printed_message_values'].tolist())