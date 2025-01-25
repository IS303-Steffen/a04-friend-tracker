#### Assignment 4
# Friend Tracker
You’ll be creating a simple python program that allows users to manage a directory of their friends' hobbies. The program will prompt the user to add new friends with their corresponding hobbies and also allow them to look up a friend's hobby.

Put your code in the `a04_friend_tracker.py` file. Do not edit or delete any other files.

## Logical Flow
Print out a menu that gives the user 3 options:
- ```
        Menu:
        1. Add a Friend
        2. Find a Friend's Hobby
        3. Quit
    ```
- Then, gather an input from the user for one of the 3 options:
    - `Enter an option (1, 2, or 3): `
    
- Then, you'll do one of the following depending on the option entered:

> ### If the user enters `1`

- Prompt the user to enter:
    - `Enter friend's name: `
- and take the input they entered and then prompt them to enter:
    - `Enter <friend's name>'s hobby`: 
- Then store that data in a dictionary, with the friend’s name as the key and the hobby as the value, and print out:
    - `<friend name> added to your dictionary!`
- But, before you add the friend/hobby to the dictionary, and before you ask `Enter <friend's name>'s hobby` check to see if that friend is already in the dictionary. If they are, don’t try to add them, and don't ask for their hobby, but instead print out:
    - `<friend name> is already in your dictionary.`

#### Tip:
- It may help to start out with an empty dictionary. You can make an empty dictionary like this:
  - `example_dictionary = {}`
- This way you have something to work with even before you have added anything to it. <br><br>FYI, you can do the same thing with lists too, but just use square brackets instead of curly brackets:
  - `example_list = []`


> ### If the user enters `2`
- Prompt the user to enter:
    - `Enter a friend's name to find their hobby: `
- After the user enters a friend's name, print this message out if the friend's name is in the dictionary:
    - `<friend name>’s hobby is <hobby>.`
- If the friend's name isn't in the dictionary, print out:
    - `<friend name> is not in the dictionary.` 

> ### If the user enters `3`
- Print out:
    - `Exiting the program. Goodbye!`

> ### If the user enters anything other than `1`, `2`, or `3`:

- Print out:
    - `Invalid choice. Please choose a valid option.`

> ### After the user completes any option:
The menu with the 3 choices should continually reappear every time choice 1, 2, or an invalid input is entered, meaning the user can input as many friends/hobbies as they want, and search for friends’ hobbies as many times as they want. The program should only end if the user enters 3 when the menu is displayed.

## Grading Rubric
See the Rubric.md file.

## Example Output
Below is an example of
- entering in 2 friends
- checking the hobby of one of the friends
- checking the hobby of a friend that doesn't exist
- trying to enter in a friend that was already added
- entering invalid input
- quitting

```
Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 1
Enter friend's name: Jimmer
Enter Jimmer's hobby: Basketball

Jimmer added to your dictionary!

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 1
Enter friend's name: Reena
Enter Reena's hobby: Listening to Sonic Youth

Reena added to your dictionary!

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 2
Enter a friend's name to find their hobby: Reena

Reena's hobby is Listening to Sonic Youth.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 2
Enter a friend's name to find their hobby: Tim

Tim is not in the dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 1
Enter friend's name: Jimmer

Jimmer is already in your dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): asdf

Invalid choice. Please choose a valid option.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```
