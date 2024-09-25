from conftest import normalize_text, load_or_reload_module

# checks if a correct dictionary is created given certain inputs

def test_3_proper_dictionary_values(mock_inputs, test_cases):
    for test_case in test_cases:
        inputs = test_case["input_values"]
        expected_dictionary = test_case["expected_dictionary_values"][0]

        # format the data into a single string (convenient for error messages)
        inputs_concatenated = '\n'.join(inputs)
        
        # Call the fixture to mock_input() with the desired inputs
        _ = mock_inputs(inputs)

        # Load the module (if it is the first test run)
        # or reload it into memory to reset global functions.
        student_globals = load_or_reload_module()
        
        # Find all variables that are of type dictionary
        student_dictionaries = {name: value for name, value in student_globals.items() if isinstance(value, dict) and name != "__builtins__"}

        # Assert that there is at least one dictionary
        assert student_dictionaries, (
            "No dictionaries found in your code.")
        
        dictionary_match_found = False
        dictionaries_string = '' # used to provide details if the test fails

        # Iterate over all dictionaries found in the student's code
        for dict_name, student_dict in student_dictionaries.items():
            dictionaries_string += f"{dict_name}: {student_dict}\n\n"
            if all(key in student_dict and student_dict[key] == value for key, value in expected_dictionary.items()):
                dictionary_match_found = True
                break  # Stop once we find a matching dictionary
        
        assert dictionary_match_found, (
            f"\nNone of the dictionaries found in your code\n"
            f"matched the expected value of the dictionary.\n\n"
            f"For these inputs:\n\n"
            f"{inputs_concatenated}\n\n"
            f"The expected value of the dictionary would be:\n\n"
            f"{expected_dictionary}\n\n"
            f"Your dictionary/dictionaries look like this:\n\n"
            f"{dictionaries_string}"
            f"Make sure you are correctly adding values to your dictionary, or\n"
            f"that you aren't tranforming the inputs in an unexpected way\n"
        )
