#### Assignment 4
# Friend Tracker
You’ll be creating a simple python program that allows users to manage a directory of their friends' hobbies. The program will prompt the user to add new friends with their corresponding hobbies and also allow them to look up a friend's hobby.

Put your code in the `a4_friend_tracker.py` file. Do not edit or delete any other files.

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
- But, before you add the friend/hobby to the dictionary, check to see if that friend is already in the dictionary. If they are, don’t try to add them, but instead print out:
    - `<friend name> is already in your dictionary.`

#### Tip:
It may help to start out with an empty dictionary. You can make an empty dictionary like this:
- `example_dictionary = {}`

This way you have something to work with even before you have added anything to it. FYI, you can do the same thing with lists too, but just use square brackets instead of curly brackets:
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
The menu with the 3 choices should continually reappear every time choice 1, 2, or an invalid 
input is entered, meaning the user can input as many friends/hobbies as they want, and search 
for friends’ hobbies. The program should only end if the user enters 3.

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
Enter friend's name: Jimmy
Enter Jimmy's hobby: Basketball

Jimmy added to your dictionary!

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
Enter friend's name: Jimmy

Jimmy is already in your dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): asdf this is invalid!

Invalid choice. Please choose a valid option.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

Make sure you code can handle this case too: immediately choosing option 2 and checking for a friend before you've added any friends. If you have trouble with this case, the tip given in the instructions about empty dictionaries might help you.
```
Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 2
Enter a friend's name to find their hobby: Jimmy

Jimmy is not in the dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

## Rubric
This assignment contains the automated tests listed below. The tests will ignore spacing, capitalization, and punctuation, but you will fail the tests if you spell something wrong or calculate something incorrectly.
<table>
<thead>
    <tr>
        <th>Test</th>
        <th>Description</th>
        <th>Points</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>1. Input Prompts</td>
        <td>You must use <code>input()</code> to ask the user the following prompts:
        <ul>
          <li><code>Enter your first name: </code></li>
        </ul>
        <ul>
          <li><code>Enter your last name: </code></li>
        </ul>
        <ul>
          <li><code>Enter the feet of your height: </code></li>
        </ul> 
        <ul>
          <li><code>Enter the inches of your height: </code></li>
        </ul> 
        <ul>
          <li><code>Enter your weight in pounds: </code></li>
        </ul>   
        </td>
        <td>15</td>
    </tr>
    <tr>
        <td>2. Printed Messages</td>
        <td>Your printed output must contain the phrase:
          <ul>
            <li><code>has a BMI of</code></li>
            <li><code>The associated category is</code></li>
          </ul>        
        </td>
        <td>15</td>
    </tr>
    <tr>
        <td>3. BMI Numerical Calculation</td>
        <td>Your printed output must contain an accurately calculated BMI.<br><br>
        The following cases will be tested:<br><br>
        <table border="1">
          <thead>
            <tr>
              <th>Input</th>
              <th>Expected Output</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>"John", "Doe", "5", "6", "114"</code></td>
              <td><code>'18.40' or '18.4'</code></td>
            </tr>
            <tr>
              <td><code>"Jane", "Smith", "5", "6", "115"</code></td>
              <td><code>"18.56"</code></td>
            </tr>
            <tr>
              <td><code>"Bob", "Brown", "5", "6", "154"</code></td>
              <td><code>"24.85"</code></td>
            </tr>
            <tr>
              <td><code>"Charlie", "Johnson", "5", "6", "185"</code></td>
              <td><code>"29.86"</code></td>
            </tr>
            <tr>
              <td><code>"Diana", "Wilson", "5", "6", "186"</code></td>
              <td><code>"30.02"</code></td>
            </tr>
          </tbody>
        </table>
        </td>
        <td>30</td>
    </tr>
        <tr>
        <td>4. BMI Categorical Calculation</td>
        <td>Your printed output must contain an accurately calculated BMI category.<br><br>
        The following cases will be tested:<br><br>
        <table border="1">
          <thead>
            <tr>
              <th>Input</th>
              <th>Expected Output</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>"John", "Doe", "5", "6", "114"</code></td>
              <td><code>"Underweight"</code></td>
            </tr>
            <tr>
              <td><code>"Jane", "Smith", "5", "6", "115"</code></td>
              <td><code>"Normal weight"</code></td>
            </tr>
            <tr>
              <td><code>"Bob", "Brown", "5", "6", "154"</code></td>
              <td><code>"Normal weight"</code></td>
            </tr>
            <tr>
              <td><code>"Charlie", "Johnson", "5", "6", "185"</code></td>
              <td><code>"Overweight"</code></td>
            </tr>
            <tr>
              <td><code>"Diana", "Wilson", "5", "6", "186"</code></td>
              <td><code>"Obese"</code></td>
            </tr>
          </tbody>
        </table>
        </td>
        <td>30</td>
    </tr>
    <tr>
        <td>5. Sufficient Comments </td>
        <td>Your code must include at least <code>5</code> comments. You can use <code>#</code>, <code>''' '''</code>, or <code>""" """</code></td>
        <td>10</td>
    </tr>
    <tr>
        <td colspan="2">Total Points</td>
        <td>100</td>
  </tr>
</tbody>
</table>
