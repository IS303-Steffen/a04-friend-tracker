max_score = 45  # Pulled by yml_generator.py to assign a score to this test.

from conftest import (
    normalize_text,
    load_student_code,
    format_error_message,
    exception_message_for_students,
    get_similarity_feedback,
    pc_get_or_create,
    pc_finalize_and_maybe_fail,
    default_module_to_test,   # keep the module used by the original test_05
)

# Checks if a correct dictionary is created given certain inputs
def test_03_proper_dictionary_values(current_test_name, input_test_cases):
    rec = pc_get_or_create(current_test_name, max_score=max_score)
    try:
       # Ensure test_cases is valid and iterable
        if not isinstance(input_test_cases, list):
            input_test_case = {"id_input_test_case": None}
            exception_message_for_students(ValueError("input_test_cases should be a list of dictionaries. Contact your professor."), input_test_case, current_test_name) 
            return  # Technically not needed, as exception_message_for_students throws a pytest.fail Error, but included for clarity that this ends the test.

        for input_test_case in input_test_cases:
            case_id = input_test_case["id_input_test_case"]
            # Skip certain test cases if needed
            if input_test_case["id_input_test_case"] in [3, 5]:
                continue

            inputs = input_test_case["inputs"]
            # This provides a dictionary of dictionaries. Each key is a variable name,
            # the value is the actual dictionary we care about.
            expected_dictionaries = input_test_case["dicts"].values()

            # Normalize expected dictionaries
            normalized_expected_dicts = []
            expected_dicts_string = ''
            for expected_dictionary in expected_dictionaries:
                if expected_dictionary is not None:
                    normalized_expected_dict = {normalize_text(key): normalize_text(value) for key, value in expected_dictionary.items()}
                    normalized_expected_dicts.append(normalized_expected_dict)

                    expected_dicts_string = ''

            for idx, normalized_expected_dict in enumerate(normalized_expected_dicts, 1):
                expected_dicts_string += f"Expected Dictionary {idx}: {normalized_expected_dict}\n\n"
            expected_dicts_string = expected_dicts_string.strip()

            # Load in the student's code and get globals
            manager_payload = load_student_code(current_test_name, inputs, input_test_case, module_to_test=default_module_to_test)
            
            if not manager_payload:
                continue # if there was an error in running student code, it's already been logged. Just skip to the next test case.

            student_variables = manager_payload.get('all_variables', {})

            # Find all variables in student's code that are of type dictionary
            student_dictionaries = {name: value for name, value in student_variables.items() if isinstance(value, dict) and name != "__builtins__" and name != "__main_locals__" and value}


            case_failed_messages = []

            # Assert that there is at least one dictionary
            if not student_dictionaries:
                formatted = format_error_message(
                    custom_message=(
                        f"The tests couldn't find any dictionary variables in your code.\n\n" 
                        f"Make sure you are storing the names/hobbies in a dictionary, or that you aren't overwriting "
                        f"your dictionary by calling another variable the same name as your dictionary.\n"),
                    current_test_name=current_test_name,
                    input_test_case=input_test_case,
                    display_inputs=True
                    )
                case_failed_messages.append(formatted)

            dictionary_match_found = False
            student_dictionaries_string = ''  # Used to provide details if the test fails

            # Iterate over all dictionaries found in the student's code
            for dict_name, student_dict in student_dictionaries.items():
                # String is useful for error reporting if test fails
                normalized_student_dict = {normalize_text(key): normalize_text(value) for key, value in student_dict.items()}
                dict_name = dict_name.rpartition(".")[-1] # the trace function capturing the dictionaries usually includes the location of the dictionary as a prefix. This cuts out the prefix.
                student_dictionaries_string += f"{dict_name}: {normalized_student_dict}\n\n"

                # Check if student_dict matches any of the expected dictionaries
                for normalized_expected_dict in normalized_expected_dicts:
                    if normalized_student_dict == normalized_expected_dict:
                        dictionary_match_found = True
                        break  # Stop once we find a matching dictionary
                if dictionary_match_found:
                    break

            if not dictionary_match_found:
                formatted = format_error_message(
                        custom_message=(
                            f"None of the dictionaries found in your code "
                            f"matched the expected dictionary for this test case.\n\n"
                            f"### Expected dictionary values:\n"
                            f"The expected dictionary values (ignoring capitalization / punctuation) are:\n"
                            f"```\n{expected_dicts_string}\n```\n"
                            f"### Your dictionary values:\n"
                            f"Your dictionary/dictionaries (ignoring capitalization / punctuation) look like this:\n"
                            f"```\n{student_dictionaries_string}\n```\n"
                            f"Make sure you are correctly adding values to your dictionary, or "
                            f"that you aren't transforming the inputs in an unexpected way.\n"),
                        current_test_name=current_test_name,
                        input_test_case=input_test_case,
                        display_inputs=True
                    )
                case_failed_messages.append(formatted)

            if case_failed_messages:
                # Join multiple messages (if both a required and invalid check failed)
                full_msg = "\n\n".join(case_failed_messages)
                rec.fail_case(case_id, custom_message=full_msg)
            else:
                rec.pass_case(case_id)

    # assert raises an AssertionError, but I don't want to actually catch it
    # this is just so I can have another Exception catch below it in case
    # anything else goes wrong.
    except AssertionError:
        raise
    
    except Exception as e:
        # Handle other exceptions
        exception_message_for_students(e, input_test_case, current_test_name)

    finally:
        # After all cases, emit a one-line summary or a short failure directing to the MD file
        pc_finalize_and_maybe_fail(rec)