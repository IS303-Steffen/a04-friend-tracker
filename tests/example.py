# def kwargs_practice(**errors_to_print):
#     error_string = ''
#     divider = "-"*76 +"\n"
#     for key, value in errors_to_print.items():
#         error_string += divider
#         error_string += str(key).upper() + "\n"

#     return error_string



# example_dict = {"inputs": [2, "Hello there", "what?"], "something else": [1,2,3], "printed_messages": ["Enter in a name", "Well, ok"]}

# print(kwargs_practice(example_dict["inputs"], example_dict["printed_messages"]))

def insert_newline_at_last_space(s, width=75):
    lines = []
    while len(s) > width:
        # Find the last space before the width limit
        break_index = s.rfind(' ', 0, width)
        
        # If no space is found, break at the width limit
        if break_index == -1:
            break_index = width
        
        # Add the line up to the break index
        lines.append(s[:break_index])
        
        # Remove the processed part of the string
        s = s[break_index:].lstrip()  # Strip leading spaces

    # Append the remainder of the string
    lines.append(s)
    
    return '\n'.join(lines)

# Example usage:
long_string = "This is a long string that you want to break into lines with a newline inserted at the last space before the 75th character."
result = insert_newline_at_last_space(long_string)
print(result)