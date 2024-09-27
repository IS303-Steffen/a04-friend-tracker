'''
Reused inputs, input prompts, messages, etc. are stored
as dictionaries with ids as the key.

Test cases are stored in a list of dictionaries, each test case a separate 
dictionary.

Each test case references those ids, which speeds up writing the test
cases.
'''
inputs_dict = {
    1: "1",
    2: "2",
    3: "3",
    4: "invalid input!",
    5: "Jimmer",
    6: "Basketball"
}

input_prompts_dict = {
    1: "Enter an option (1, 2, or 3): ",
    2: "Enter friend's name: ",
    3: "Enter {wildcard}'s hobby: ",
    4: "Enter a friend's name to find their hobby: ",
    5: "Enter Jimmer's hobby: "
}

printed_messages_dict = {
    1: "Menu: ",
    2: "1. Add a Friend",
    3: "2. Find a Friend's Hobby",
    4: "3. Quit",
    5: "{wildcard} is already in your dictionary.",
    6: "{wildcard} added to your dictionary!",
    7: "{wildcard}'s hobby is {wildcard}.",
    8: "{wildcard} is not in the dictionary.",
    9: "Exiting the program. Goodbye!",
    10: "Invalid choice. Please choose a valid option.",
    11: "Jimmer added to your dictionary!",
    12: "Jimmer's hobby is Basketball.",
    13: "Jimmer is already in your dictionary.",
}

dictionaries_dict = {
    1: None,
    2: {},
    3: {"Jimmer": "Basketball"},
}

# A function to resolve the IDs into actual values
# references the global dictionaries defined above.
def add_values_to_test_case(test_case):
    test_case['input_values'] = [inputs_dict[i] for i in test_case['input_ids']]
    test_case['expected_input_prompt_values'] = [input_prompts_dict[i] for i in test_case['expected_input_prompt_ids']]
    test_case['invalid_input_prompt_values'] = [input_prompts_dict[i] for i in input_prompts_dict if i not in test_case['expected_input_prompt_ids']]
    test_case['expected_printed_message_values'] = [printed_messages_dict[i] for i in test_case['expected_printed_message_ids']]
    test_case['invalid_printed_message_values'] = [printed_messages_dict[i] for i in printed_messages_dict if i not in test_case['expected_printed_message_ids']]
    test_case['expected_dictionary_values'] = [dictionaries_dict[i] for i in test_case['expected_dictionary_ids']]
    return test_case

# Test cases with references by ID
test_cases_list = [
    { # 1: Invalid input choice
    'id_test_case': 1,
    'test_description': '1: Invalid input choice',
    'input_ids': [4, 3],  
    'expected_input_prompt_ids': [1], 
    'expected_printed_message_ids': [1, 2, 3, 4, 9, 10],
    'expected_dictionary_ids': [1,2], 
    },
    { # 2: Single name/hobby, no lookup
    'id_test_case': 2,
    'test_description': '2: Single name/hobby, no lookup',
    'input_ids': [1, 5, 6, 3],  
    'expected_input_prompt_ids': [1, 2, 3, 5], 
    'expected_printed_message_ids': [1, 2, 3, 4, 6, 9, 11],
    'expected_dictionary_ids': [3], 
    },
    { # 3: Single name/hobby, w/ lookup
    'id_test_case': 3,
    'test_description': '3: Single name/hobby, w/ lookup',
    'input_ids': [1, 5, 6, 2, 5, 3],  
    'expected_input_prompt_ids': [1, 2, 3, 5, 4], 
    'expected_printed_message_ids': [1, 2, 3, 4, 9, 6, 11, 7, 12],
    'expected_dictionary_ids': [3], 
    },
    { # 4: Single name/hobby, entering name twice
    'id_test_case': 4,
    'test_description': '4: Single name/hobby, entering name twice',
    'input_ids': [1, 5, 6, 1, 5, 3],  
    'expected_input_prompt_ids': [1, 2, 3, 5], 
    'expected_printed_message_ids': [1, 2, 3, 4, 5, 13, 9, 6, 11, 7, 12],
    'expected_dictionary_ids': [3], 
    },
]
# adding values to each test case
test_cases_list = [add_values_to_test_case(test_case) for test_case in test_cases_list]
#return test_cases_list