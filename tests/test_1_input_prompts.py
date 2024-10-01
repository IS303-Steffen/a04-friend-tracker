max_score = 25  # This value is pulled by yml_generator.py to assign a score to this test.
from conftest import normalize_text, load_or_reload_module, format_error_message, exception_message_for_students, timeout_counter, timeout_message_for_students
from conftest import default_timeout_seconds
import re, multiprocessing, pytest, os

# checks if the input prompts (from using input()) contain the expected prompts.
def test_1_input_prompts(mock_inputs, test_cases):
    try:
        # creates a boolean that can be passed around different processes
        # used in the KeyboardInterrupt Exception, since that is the error I trigger if a timeout occurs
        timeout_triggered = multiprocessing.Value('b', 0)

        # Ensure test_cases is valid and iterable
        if not isinstance(test_cases, list):
            raise ValueError("test_cases should be a list of dictionaries. Contact your professor.")

        # Loop through each test case
        for test_case in test_cases:
            main_pid = os.getpid() # Grab the process id, in case the main process needs to be shutdown during timeout
            stop_counting_event = multiprocessing.Event()

            # create the process for running a counter
            timeout_counter_thread = multiprocessing.Process(target=timeout_counter, args=(stop_counting_event, main_pid, timeout_triggered))
            timeout_counter_thread.start()
            
            try:
                # grab the necessary data from the test case dictionary
                inputs = test_case["inputs"]
                expected_input_prompts = test_case["input_prompts"]
                invalid_input_prompts = test_case["invalid_input_prompts"]

                # Load in the student's code
                captured_input_prompts, _ = load_or_reload_module(mock_inputs, inputs, test_case)

                # Normalize the captured input prompts to remove spaces, punctuation, and symbols
                normalized_captured_input_prompts = [normalize_text(captured_prompt) for captured_prompt in captured_input_prompts]
                normalized_captured_input_prompts = '\n'.join(normalized_captured_input_prompts)

                # Check that each required phrase (regex pattern) is found in the normalized captured output
                for expected_phrase in expected_input_prompts:
                    expected_phrase = normalize_text(expected_phrase)
                    regex_pattern = expected_phrase.replace("wildcard", r".+?")
                    match = re.search(regex_pattern, normalized_captured_input_prompts)

                    assert match, format_error_message(
                        custom_message=("The expected input prompt (ignoring punctuation / capitalization):\n\n"
                                        f"\"{expected_phrase}\"\n\n"
                                        f"wasn't found in the input() function output.\n\n"
                                        f"Below are all the input prompts from your code (ignoring punctuation / capitalization):\n\n"
                                        f"{normalized_captured_input_prompts}\n\n"),
                        test_case=test_case,
                        display_inputs=True,
                        display_input_prompts=True,
                        display_invalid_input_prompts=True
                    )

                # Ensure none of the invalid phrases are found in the normalized captured output
                for invalid_phrase in invalid_input_prompts:
                    invalid_phrase = normalize_text(invalid_phrase)
                    regex_pattern = invalid_phrase.replace("wildcard", r".+?")
                    match = re.search(regex_pattern, normalized_captured_input_prompts)

                    assert not match, format_error_message(
                        custom_message=("You used an invalid input() prompt (ignoring punctuation / capitalization):\n\n"
                                        f"\"{invalid_phrase}\"\n\n"
                                        f"Below are all the input prompts from your code (ignoring punctuation / capitalization):\n\n"
                                        f"{normalized_captured_input_prompts}\n\n"),
                        test_case=test_case,
                        display_inputs=True,
                        display_input_prompts=True,
                        display_invalid_input_prompts=True
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