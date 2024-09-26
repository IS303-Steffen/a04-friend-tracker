import numpy
import re

# Name: Jacob Steffen
# Description: This allows you to enter friend's names and their hobby,
# then look up the friend and hobby.

def example_code():
    return 2+2

if __name__ == "__main__":

    friends_hobbies = {}
    continue_prompting = True

    while continue_prompting:
        print("\nMenu:")
        print("1. Add a Friend")
        print("2. Find a Friend's Hobby")
        print("3. Quit")

        choice = input("Enter an option (1, 2, or 3): ")
        if choice == '1':
            # Add a friend
            name = input("Enter friend's name: ")
            if name in friends_hobbies:
                print(f"\n{name} is already in your dictionary.")
            else:
                hobby = input(f"Enter {name}'s hobby: ")
                friends_hobbies[name] = hobby
                print(f"\n{name} added to your dictionary!")
        
        elif choice == '2':
            # Find a friend's hobby
            name = input("Enter a friend's name to find their hobby: ")
            if name in friends_hobbies:
                print(f"\n{name}'s hobby is {friends_hobbies[name]}.")
            else:
                print(f"\n{name} is not in the dictionary.")
        
        elif choice == '3':
            # Quit the program
            print("\nExiting the program. Goodbye!")
            continue_prompting = False
        else:
            print("\nInvalid choice. Please choose a valid option.")

def another_example():
    print("Wow this really works!")

another_example()