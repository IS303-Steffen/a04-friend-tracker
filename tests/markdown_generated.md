### All Possible Input Prompts:
- `Enter Jimmer's hobby: `
- `Enter Link's hobby: `
- `Enter Reena's hobby: `
- `Enter a friend's name to find their hobby: `
- `Enter an option (1, 2, or 3): `
- `Enter friend's name: `

### All Possible Printed Messages:
- `Exiting the program. Goodbye!`
- `Invalid choice. Please choose a valid option.`
- `Jimmer added to your dictionary!`
- `Jimmer is already in your dictionary.`
- `Jimmer is not in the dictionary.`
- `Jimmer's hobby is Basketball.`
- `Link added to your dictionary!`
- `Menu:`
- `Reena added to your dictionary!`
- `Reena's hobby is Listening to Sonic Youth.`
- `1. Add a Friend`
- `2. Find a Friend's Hobby`
- `3. Quit`

## Test Cases Summary
<table>
  <tr>
    <th>Test Case Description</th>
    <th>Inputs</th>
  </tr>
  <tr>
    <td><a href="#testcase1">1: Single name/hobby, no lookup</a></td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td><a href="#testcase2">2: Single name/hobby with lookup</a></td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>2</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td><a href="#testcase3">3: Invalid input</a></td>
    <td><ul>
  <li><code>INVALID INPUT!</code></li>
  <li><code>4</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td><a href="#testcase4">4: Single name/hobby, repeat name</a></td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td><a href="#testcase5">5: Lookup before entering name/hobby</a></td>
    <td><ul>
  <li><code>2</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td><a href="#testcase6">6: Multiple friends/hobbies</a></td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>1</code></li>
  <li><code>Reena</code></li>
  <li><code>Listening to Sonic Youth</code></li>
  <li><code>1</code></li>
  <li><code>Link</code></li>
  <li><code>Breaking pots</code></li>
  <li><code>2</code></li>
  <li><code>Reena</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
</table>

<h3 id="testcase1">Test Case 1 Details - Single name/hobby, no lookup</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Jimmer's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td><ul>
  <li><code>Enter a friend's name to find their hobby:</code></li>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Jimmer is already in your dictionary.</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Link added to your dictionary!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{"Jimmer": "Basketball"}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

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
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

<h3 id="testcase2">Test Case 2 Details - Single name/hobby with lookup</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>2</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Jimmer's hobby:</code></li>
  <li><code>Enter a friend's name to find their hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td><ul>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer is already in your dictionary.</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Link added to your dictionary!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{"Jimmer": "Basketball"}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

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
Enter an option (1, 2, or 3): 2
Enter a friend's name to find their hobby: Jimmer

Jimmer's hobby is Basketball.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

<h3 id="testcase3">Test Case 3 Details - Invalid input</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>INVALID INPUT!</code></li>
  <li><code>4</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td><ul>
  <li><code>Enter a friend's name to find their hobby:</code></li>
  <li><code>Enter Jimmer's hobby:</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Jimmer is already in your dictionary.</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Link added to your dictionary!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

```
Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): INVALID INPUT!

Invalid choice. Please choose a valid option.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 4

Invalid choice. Please choose a valid option.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

<h3 id="testcase4">Test Case 4 Details - Single name/hobby, repeat name</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Jimmer's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td><ul>
  <li><code>Enter a friend's name to find their hobby:</code></li>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Jimmer is already in your dictionary.</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Link added to your dictionary!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{"Jimmer": "Basketball"}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

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

<h3 id="testcase5">Test Case 5 Details - Lookup before entering name/hobby</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>2</code></li>
  <li><code>Jimmer</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
  <li><code>Enter a friend's name to find their hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td><ul>
  <li><code>Enter Jimmer's hobby:</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Jimmer is already in your dictionary.</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Link added to your dictionary!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

```
Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 2
Enter a friend's name to find their hobby: Jimmer

Jimmer is not in the dictionary.

Menu:
1. Add a Friend
2. Find a Friend's Hobby
3. Quit
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

<h3 id="testcase6">Test Case 6 Details - Multiple friends/hobbies</h3>

<table>
  <tr>
    <th>Requirement</th>
    <th>Components</th>
  </tr>
  <tr>
    <td>Inputs</td>
    <td><ul>
  <li><code>1</code></li>
  <li><code>Jimmer</code></li>
  <li><code>Basketball</code></li>
  <li><code>1</code></li>
  <li><code>Reena</code></li>
  <li><code>Listening to Sonic Youth</code></li>
  <li><code>1</code></li>
  <li><code>Link</code></li>
  <li><code>Breaking pots</code></li>
  <li><code>2</code></li>
  <li><code>Reena</code></li>
  <li><code>3</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Input Prompts</td>
    <td><ul>
  <li><code>Enter an option (1, 2, or 3):</code></li>
  <li><code>Enter friend's name:</code></li>
  <li><code>Enter Jimmer's hobby:</code></li>
  <li><code>Enter Reena's hobby:</code></li>
  <li><code>Enter Link's hobby:</code></li>
  <li><code>Enter a friend's name to find their hobby:</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Input Prompts</td>
    <td></td>
  </tr>
  <tr>
    <td>Printed Messages</td>
    <td><ul>
  <li><code>Menu:</code></li>
  <li><code>1. Add a Friend</code></li>
  <li><code>2. Find a Friend's Hobby</code></li>
  <li><code>3. Quit</code></li>
  <li><code>Jimmer added to your dictionary!</code></li>
  <li><code>Reena added to your dictionary!</code></li>
  <li><code>Link added to your dictionary!</code></li>
  <li><code>Reena's hobby is Listening to Sonic Youth.</code></li>
  <li><code>Exiting the program. Goodbye!</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Invalid Printed Messages</td>
    <td><ul>
  <li><code>Jimmer's hobby is Basketball.</code></li>
  <li><code>Jimmer is not in the dictionary.</code></li>
  <li><code>Invalid choice. Please choose a valid option.</code></li>
  <li><code>Jimmer is already in your dictionary.</code></li>
</ul></td>
  </tr>
  <tr>
    <td>Dicts</td>
    <td><ul>
  <li><code>{"Jimmer": "Basketball", "Reena": "Listening to Sonic Youth", "Link": "Breaking pots"}</code></li>
</ul></td>
  </tr>
</table>

<h4>Example Ouput:</h4>

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
Enter an option (1, 2, or 3): 3

Exiting the program. Goodbye!
```

