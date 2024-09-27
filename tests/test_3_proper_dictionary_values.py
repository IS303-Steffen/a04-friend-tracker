max_score = 45 # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module

# checks if a correct dictionary is created given certain inputs

def test_3_proper_dictionary_values(mock_inputs, test_cases):
    for test_case in test_cases:
        inputs = test_case["input_values"]
        expected_dictionaries = test_case["expected_dictionary_values"]

        # format the data into a single string (convenient for error messages)
        inputs_concatenated = '\n'.join(inputs)
        
        # Load in the student's code (which runs anything at a global level)
        # By passing in mock_inputs, the student's input() function will be
        # replaced by a mock version that will auto insert the inputs for the 
        # test case

        _, student_globals = load_or_reload_module(mock_inputs, inputs)
        
        # Find all variables in student's code that are of type dictionary
        student_dictionaries = {name: value for name, value in student_globals.items() if isinstance(value, dict) and name != "__builtins__"}
        if test_case["id_test_case"] not in [1]:
            # Assert that there is at least one dictionary
            assert student_dictionaries, (
                "No dictionaries found in your code.")
        
        dictionary_match_found = False
        dictionaries_string = '' # used to provide details if the test fails

       # Iterate over all dictionaries found in the student's code
        for dict_name, student_dict in student_dictionaries.items():
            # string is useful for error reporting if test fails
            dictionaries_string += f"{dict_name}: {student_dict}\n\n"
            
            # Check if student_dict matches any of the expected dictionaries
            for expected_dictionary in expected_dictionaries:
                if expected_dictionary is not None:
                    if all(key in student_dict and student_dict[key] == value for key, value in expected_dictionary.items()):
                        dictionary_match_found = True
                        break  # Stop once we find a matching dictionary
            if dictionary_match_found:
                break

        assert dictionary_match_found, (
            f"\nNone of the dictionaries found in your code\n"
            f"matched the expected value of any dictionary in the list.\n\n"
            f"For these inputs:\n\n"
            f"{inputs_concatenated}\n\n"
            f"The expected value of one of the dictionaries would be:\n\n"
            f"{expected_dictionaries}\n\n"
            f"Your dictionary/dictionaries look like this:\n\n"
            f"{dictionaries_string}"
            f"Make sure you are correctly adding values to your dictionary, or\n"
            f"that you aren't transforming the inputs in an unexpected way\n"
)
