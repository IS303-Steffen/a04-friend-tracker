
# Rubric
Your grade is based on whether you pass the automated tests, listed below.

The tests will ignore spacing, capitalization, and punctuation, but you will fail the tests if you spell something wrong or calculate something incorrectly.

<table border="1" style="width: 100%; text-align: center;">
<thead>
    <tr>
        <th style="text-align: center;">Test</th>
        <th style="text-align: center;">Description</th>
        <th style="text-align: center;">Points</th>
    </tr>
</thead>
<tbody>
    <tr style="text-align: left">
        <td>1. Input Prompts</td>
        <td>
        <b>Input test cases used:</b> 1-6<br><br>
        Your input prompts must be the same as the expected input prompts of each input test case. 
        <br>
        <br>
        See the <code>descriptions_ot_test_cases</code> folder for expected input prompts for each input test case.
        </td> 
        <td>25</td>
    </tr>
    <tr style="text-align: left">
        <td>2. Printed Messages</td>
        <td>
        <b>Input test cases used:</b> 1-5<br><br>
        Your printed output must be the same as the expected output of each input test case. This includes the correct BMI calculations and BMI categories.
        <br>
        <br>
        See the <code>descriptions_ot_test_cases</code> folder for expected printed messages for each input test case.       
        </td>
        <td>25</td>
    </tr>
        <tr style="text-align: left">
        <td>3. Printed Messages</td>
        <td>
        <b>Input test cases used:</b> 1, 2, 4, 6<br><br>
        Your code must store the inputted friend names and hobbies in a dictionary variable, with the friend names as the key and the hobbies as the values. It doesn't matter what you call the variable.
        <br>
        <br>
        See the <code>descriptions_ot_test_cases</code> folder for inputs used in each test case to see what your dictionaries should hold.    
        </td>
        <td>45</td>
    </tr>
    <tr style="text-align: left">
        <td>4. Sufficient Comments </td>
        <td>
        <b>Input test cases used:</b> None<br><br>
        Your code must include at least <code>5</code> comments. You can use any form of commenting:
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
If you fail a test during a specific test case, see the `descriptions_of_test_cases` folder for the following:
<table border="1" style="width: 100%; text-align: left;">
  <tr>
    <th>Test Case</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Input Test Case 01</td>
    <td>Entering a single name/hobby and exiting</td>
  </tr>
  <tr>
    <td>Input Test Case 02</td>
    <td>Entering a single name/hobby then looking that friend up</td>
  </tr>
  <tr>
    <td>Input Test Case 03</td>
    <td>Entering invalid input strings and then exiting.</td>
  </tr>
  <tr>
    <td>Input Test Case 04</td>
    <td>Entering a name/hobby, then entering the same name to see if it prevents entering twice</td>
  </tr>
  <tr>
    <td>Input Test Case 05</td>
    <td>Looking up a name that doesn't exist before entering any names.</td>
  </tr>
  <tr>
    <td>Input Test Case 06</td>
    <td>Entering multiple friends/hobbies and looking them up.</td>
  </tr>
</table>