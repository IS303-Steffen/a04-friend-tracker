import re
from conftest import module_to_test

def test_5_sufficient_comments():
    required_num_comments = 5
    # Open and read the student's script as a string
    with open(f"{module_to_test}.py", "r") as file:
        script_content = file.read()

    # Regex to match single-line comments (#) and multi-line comments (''' ''' or """ """)
    # . is any character except new line
    # * means 0 or many occurrences of the previous character
    # \s means spaces \S is any non-space character, meaning it gets everything including new lines
    # *? is a non-greedy match
    comment_pattern = r"(#.*)|('''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"

    # Find all matches for comments
    comments = re.findall(comment_pattern, script_content)

    # Count total number of comments
    num_comments = len(comments)

    # Ensure there are at least 3 comments
    assert num_comments >= required_num_comments, f"\n\nNot enough comments found. You need at least {required_num_comments}. Only {num_comments} comment(s) detected."