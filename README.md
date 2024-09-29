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

This way you have something to work with even before you have added anything to it. <br><br>FYI, you can do the same thing with lists too, but just use square brackets instead of curly brackets:
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

After this table, see the Test Cases table below to see what inputs will be run for each of the tests below. To receive points for a test, the test must pass each of the individual test cases.

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
        <td>All the these tests are expecting 4 <code>input()</code> prompts to be present in your code. You must use <code>input()</code> to ask the user the following prompts, depending on the input the user provides:
        <ul>
          <li><code>Enter an option (1, 2, or 3):  </code></li>
        </ul>
        <ul>
          <li><code>Enter friend's name:  </code></li>
        </ul>
        <ul>
          <li><code>Enter &lt;Friend's name&gt;'s hobby: : </code></li>
        </ul>
        <ul>
          <li><code>Enter a friend's name to find their hobby: </code></li>
        </ul> 
        </td>
        <td>25</td>
    </tr>
    <tr>
        <td>2. Printed Messages</td>
        <td>Your printed output must contain these phrases, though only some should print out depending on what the user inputs:
          <ul>
            <li><code>Menu:</code></li>
            <li><code>1. Add a Friend</code></li>
            <li><code>2. Find a Friend's Hobby</code></li>
            <li><code>3. Quit</code></li>
            <li><code>&lt;Friend's name&gt; is already in your dictionary.</code></li>
            <li><code>&lt;Friend's name&gt; added to your dictionary!</code></li>
            <li><code>&lt;Friend's name&gt;'s hobby is &lt;Friend's hobby&gt;.</code></li>
            <li><code>&lt;Friend's name&gt; is not in the dictionary.</code></li>
            <li><code>Exiting the program. Goodbye!</code></li>
            <li><code>Invalid choice. Please choose a valid option.</code></li>
          </ul>        
        </td>
        <td>25</td>
    </tr>
    <tr>
        <td>3. Creation of Dictionary</td>
        <td>Your code must store friends' names and hobbies in a dictionary data type. See the test cases section for examples.
        </td>
        <td>45</td>
    </tr>
    <tr>
        <td>4. Sufficient Comments </td>
        <td>Your code must include at least <code>5</code> comments. You can use any form of commenting:
        <ul>
          <li><code>#</code></li> 
          <li><code>''' '''</code></li>
          <li><code>""" """</code></li>
        </ul>
        </td>
        <td>5</td>
    </tr>
    <tr>
        <td colspan="2">Total Points</td>
        <td>100</td>
  </tr>
</tbody>
</table>

## Test Cases
Each of the below test cases will be run on the above tests. Your code should function properly when entering the provided inputs.

<table border="1">
    <thead>
        <tr>
            <th>Description</th>
            <th>Input</th><th>Expected Output: dicts</th></tr>
    </thead>
    <tbody><tr>
            <td>1. Single name/hobby, no lookup</td>
            <td><code>"1", "Jimmer", "Basketball", "3"</code></td><td><code>{"Jimmer": "Basketball"}</code></td></tr><tr>
            <td>2. Single name/hobby with lookup</td>
            <td><code>"1", "Jimmer", "Basketball", "2", "Jimmer", "3"</code></td><td><code>{"Jimmer": "Basketball"}</code></td></tr><tr>
            <td>3. Invalid input</td>
            <td><code>"INVALID INPUT!", "4", "3"</code></td><td><code>{}</code> or <code>None</code></td></tr><tr>
            <td>4. Single name/hobby, repeat name</td>
            <td><code>"1", "Jimmer", "Basketball", "1", "Jimmer", "3"</code></td><td><code>{"Jimmer": "Basketball"}</code></td></tr><tr>
            <td>5. Lookup before entering name/hobby</td>
            <td><code>"2", "Jimmer", "3"</code></td><td><code>{}</code> or <code>None</code></td></tr><tr>
            <td>6. Multiple friends/hobbies</td>
            <td><code>"1", "Jimmer", "Basketball", "1", "Reena", "Listening to Sonic Youth", "1", "Link", "Breaking pots", "2", "Reena", "3"</code></td><td><code>{"Jimmer": "Basketball", "Reena": "Listening to Sonic Youth", "Link": "Breaking pots"}</code></td></tr></tbody>
</table>