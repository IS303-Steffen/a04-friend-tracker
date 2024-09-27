max_score = 25 # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module
import re

# checks if the input prompts (from using input()) contain the expected prompts.

def test_1_input_prompts(mock_inputs, test_cases):
    # test_cases is a list of dictionaries. Each dictionary represents a test case
    for test_case in test_cases:
        # grab the necessary data from the test case dictionary
        inputs = test_case["input_values"]
        expected_input_prompts = test_case["expected_input_prompt_values"]
        invalid_input_prompts = test_case["invalid_input_prompt_values"]

        # format the data into a single string (convenient for error messages)
        inputs_concatenated = '\n'.join(inputs)
        expected_input_prompts_concatenated = '\n'.join(expected_input_prompts)
        invalid_input_prompts_concatenated = '\n'.join(invalid_input_prompts)

        # Load in the student's code (which runs anything at a global level)
        # By passing in mock_inputs, the student's input() function will be
        # replaced by a mock version that will auto insert the inputs for the 
        # test case

        captured_input_prompts, _ = load_or_reload_module(mock_inputs, inputs)
        
        # Normalize the captured input prompts to remove spaces, punctuation, and symbols
        normalized_captured_input_prompts = [normalize_text(captured_prompt) for captured_prompt in captured_input_prompts]
        normalized_captured_input_prompts = '\n'.join(normalized_captured_input_prompts)

        # puts the inputs into one string for a better error message if it fails.
        

        # Check that each required phrase (regex pattern) is found in the normalized captured output
        for expected_phrase in expected_input_prompts:
            # Ensure the expected phrase is normalized as well
            expected_phrase = normalize_text(expected_phrase)
            
            # Convert the expected phrase into a regex pattern (replace {name} with a regex wildcard for any text)
            regex_pattern = expected_phrase.replace("wildcard", r".+?")
            
            # Check if the pattern exists in the normalized captured input prompts
            match = re.search(regex_pattern, normalized_captured_input_prompts)

            assert match, (
                f"\n------------------------------------------------------------\n"
                f"ERROR DESCRIPTION\n"
                f"Test case {test_case["test_description"]}\n\n"
                f"The expected input prompt\n"
                f"(ignoring punctuation / capitalization):\n\n"
                f"\"{expected_phrase}\"\n\n"
                f"wasn't found in the input() function output.\n\n"
                f"Below are all the input prompts from your code:\n"
                f"(ignoring punctuation / capitalization):\n\n"
                f"{normalized_captured_input_prompts}\n\n"
                f"------------------------------------------------------------\n"
                f"INPUTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Enters these inputs in this order:\n\n"
                f"{inputs_concatenated}\n"
                f"------------------------------------------------------------\n"
                f"EXPECTED INPUT PROMPTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Expects these input prompts:\n\n"
                f"{expected_input_prompts_concatenated}\n"
                f"------------------------------------------------------------\n"
                f"INVALID INPUT PROMPTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Doesn't allow these invalid input prompts:\n\n"
                f"{invalid_input_prompts_concatenated}\n"
                )

        # Ensure none of the invalid phrases are found in the normalized captured output
        for invalid_phrase in invalid_input_prompts:
            # Ensure the expected phrase is normalized as well
            invalid_phrase = normalize_text(invalid_phrase)
            
            # Convert the expected phrase into a regex pattern (replace {name} with a regex wildcard for any text)
            regex_pattern = invalid_phrase.replace("wildcard", r".+?")
            
            # Check if the pattern exists in the normalized captured input prompts
            match = re.search(regex_pattern, normalized_captured_input_prompts)

            assert not match, (
                f"\n------------------------------------------------------------\n"
                f"ERROR DESCRIPTION\n"
                f"Test case {test_case["test_description"]}\n\n"
                f"You used an invalid input() prompt\n"
                f"(ignoring punctuation / capitalization):\n\n"
                f"\"{invalid_phrase}\"\n\n"
                f"Below are all the input prompts from your code\n"
                f"(ignoring punctuation / capitalization):\n\n"
                f"{normalized_captured_input_prompts}\n\n"
                f"------------------------------------------------------------\n"
                f"INPUTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Enters these inputs in this order:\n\n"
                f"{inputs_concatenated}\n"
                f"------------------------------------------------------------\n"
                f"EXPECTED INPUT PROMPTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Expects these input prompts:\n\n"
                f"{expected_input_prompts_concatenated}\n"
                f"------------------------------------------------------------\n"
                f"INVALID INPUT PROMPTS\n"
                f"Test case {test_case["test_description"]}\n"
                f"Doesn't allow these invalid input prompts:\n\n"
                f"{invalid_input_prompts_concatenated}\n"
                )
