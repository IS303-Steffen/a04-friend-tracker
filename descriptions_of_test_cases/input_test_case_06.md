# Test Case 6

## Description
Entering multiple friends/hobbies and looking them up.

## Inputs
```
1: "1"
2: "Jimmer"
3: "Basketball"
4: "1"
5: "Reena"
6: "Listening to Sonic Youth"
7: "1"
8: "Link"
9: "Breaking pots"
10: "2"
11: "Reena"
12: "2"
13: "Link"
14: "3"
```

## Expected Input Prompts
```
1: "Enter an option (1, 2, or 3): "
2: "Enter friend's name: "
3: "Enter Jimmer's hobby: "
4: "Enter Reena's hobby: "
5: "Enter Link's hobby: "
6: "Enter a friend's name to find their hobby: "
```

## Expected Printed Messages
```
1: "Menu:"
2: "1. Add a Friend"
3: "2. Find a Friend's Hobby"
4: "3. Quit"
5: "Jimmer added to your dictionary!"
6: "Reena added to your dictionary!"
7: "Link added to your dictionary!"
8: "Reena's hobby is Listening to Sonic Youth."
9: "Link's hobby is Breaking pots."
10: "Exiting the program. Goodbye!"
```

## Example Output **(combined Inputs, Input Prompts, and Printed Messages)**
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
Enter an option (1, 2, or 3): 1
Enter friend's name: Link
Enter Link's hobby: Breaking pots

Link added to your dictionary!

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
Enter a friend's name to find their hobby: Link

Link's hobby is Breaking pots.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```
