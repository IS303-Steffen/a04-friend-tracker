# Test Case 4

## Description
Entering a name/hobby, then entering the same name to see if it prevents entering twice

## Inputs
```
1: "1"
2: "Jimmer"
3: "Basketball"
4: "1"
5: "Jimmer"
6: "3"
```

## Expected Input Prompts
```
1: "Enter an option (1, 2, or 3): "
2: "Enter friend's name: "
3: "Enter Jimmer's hobby: "
```

## Expected Printed Messages
```
1: "Menu:"
2: "1. Add a Friend"
3: "2. Find a Friend's Hobby"
4: "3. Quit"
5: "Jimmer added to your dictionary!"
6: "Jimmer is already in your dictionary."
7: "Exiting the program. Goodbye!"
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
Enter friend's name: Jimmer

Jimmer is already in your dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```
