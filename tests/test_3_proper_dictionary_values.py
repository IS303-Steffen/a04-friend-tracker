max_score = 45 # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module, format_error_message, exception_message_for_students, timeout_counter, timeout_message_for_students
from conftest import default_timeout_seconds
import multiprocessing, pytest, os

# checks if a correct dictionary is created given certain inputs

def test_3_proper_dictionary_values(mock_inputs, test_cases):
    try:
        # creates a boolean that can be passed around different processes
        # used in the KeyboardInterrupt Exception, since that is the error I trigger if a timeout occurs
        timeout_triggered = multiprocessing.Value('b', 0)

        # Ensure test_cases is valid and iterable
        if not isinstance(test_cases, list):
            raise ValueError("test_cases should be a list of dictionaries. Contact your professor.")   

        for test_case in test_cases:
            main_pid = os.getpid() # Grab the process id, in case the main process needs to be shutdown during timeout
            stop_counting_event = multiprocessing.Event()

            # create the process for running a counter
            timeout_counter_thread = multiprocessing.Process(target=timeout_counter, args=(stop_counting_event, main_pid, timeout_triggered))
            timeout_counter_thread.start()
            try:

                if test_case["id_test_case"] in [3,5]:
                    continue
                
                inputs = test_case["inputs"]
                # this provides a dictionary of dictionaries. Each key is a variable name,
                # the value is the actual dicitonary we care about.
                expected_dictionaries = test_case["dicts"].values()
                
                # Load in the student's code (which runs anything at a global level)
                # By passing in mock_inputs, the student's input() function will be
                # replaced by a mock version that will auto insert the inputs for the 
                # test case

                _, student_globals = load_or_reload_module(mock_inputs, inputs, test_case)
                
                # Find all variables in student's code that are of type dictionary
                student_dictionaries = {name: value for name, value in student_globals.items() if isinstance(value, dict) and name != "__builtins__"}
                
                # if there isn't even a dictionary, fail the test now
                
                # Assert that there is at least one dictionary
                assert student_dictionaries, (
                    "No dictionaries found in your code.")
                
                dictionary_match_found = False
                student_dictionaries_string = '' # used to provide details if the test fails

                # Iterate over all dictionaries found in the student's code
                for dict_name, student_dict in student_dictionaries.items():
                    # string is useful for error reporting if test fails
                    normalized_student_dict = {normalize_text(key): normalize_text(value) for key, value in student_dict.items()}

                    student_dictionaries_string += f"{dict_name}: {normalized_student_dict}\n\n"
                    
                    # Check if student_dict matches any of the expected dictionaries
                    for expected_dictionary in expected_dictionaries:
                        if expected_dictionary is not None:
                            # Normalize keys and values in both dictionaries for comparison
                            normalized_expected_dict = {normalize_text(key): normalize_text(value) for key, value in expected_dictionary.items()}
                            
                            if all(key in normalized_student_dict and normalized_student_dict[key] == value for key, value in normalized_expected_dict.items()) and \
                            all(key in normalized_expected_dict and normalized_expected_dict[key] == value for key, value in normalized_student_dict.items()):
                                dictionary_match_found = True
                                break  # Stop once we find a matching dictionary
                    if dictionary_match_found:
                        break

                assert dictionary_match_found, format_error_message(
                    custom_message=(
                    f"None of the dictionaries found in your code "
                    f"matched any of the expected values for dictionaries in this test case. "
                    f"The expected values (ignoring capitalization / punctuation) are:\n\n"
                    f"{normalized_expected_dict}\n\n"
                    f"Your dictionary/dictionaries (ignoring capitalization / punctuation) look like this:\n\n"
                    f"{student_dictionaries_string}"
                    f"Make sure you are correctly adding values to your dictionary, or "
                    f"that you aren't transforming the inputs in an unexpected way\n"),
                    test_case=test_case,
                    display_inputs=True
                    )
            except KeyboardInterrupt:
                # Check if the timeout flag was set
                if timeout_triggered.value == 1:
                    print("Process interrupted due to timeout.")
                    pytest.fail(
                        timeout_message_for_students(test_case))
                    
                else:
                    print("Process interrupted by user (Ctrl+C).")

            except Exception as e:
                exception_message_for_students(e, test_case)

            finally:
                # Ensure the counter process is stopped properly
                if timeout_counter_thread.is_alive():
                    stop_counting_event.set()  # Signal the counter thread to stop
                    timeout_counter_thread.join()  # Wait for the thread to finish


    except Exception as outer_e:
        # Handle problems with test_cases (e.g., invalid type or structure)
        test_case = {"id_test_case": None}
        exception_message_for_students(outer_e, test_case=test_case)  # Pass `None` since test_case is not valid