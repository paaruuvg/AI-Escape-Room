# Test cases — Word Puzzle Version

# Application Testing and Test Cases

## 1. Introduction

The Medieval Castle Escape Room application was tested to verify that the puzzles, answer validation, game progress, countdown timer and final escape functionality work correctly.

Testing was performed to identify incorrect behaviour and challenging situations that could affect the player's experience.

Version 2 improves reliability by separating the game logic from the Streamlit user interface and using independent validation functions.

## 2. Test Cases

The following test cases cover normal gameplay, incorrect inputs and challenging situations.

| Test ID | Test scenario | Input / Action | Expected result |
|---|---|---|---|
| TC01 | Correct puzzle answer | Examine an object and enter its correct answer | The answer is accepted and the corresponding letter is collected |
| TC02 | Incorrect puzzle answer | Enter an incorrect word | The answer is rejected and the player does not receive a letter |
| TC03 | Solve without examining | Submit an answer before examining the object | The action is rejected because the object has not been examined |
| TC04 | Unknown object | Attempt to interact with an object that does not exist | The application handles the invalid object without crashing |
| TC05 | Final gate before completing puzzles | Enter ESCAPE before collecting all six letters | The gate remains locked |
| TC06 | Successful escape | Solve all six puzzles, arrange the letters and enter ESCAPE | The final gate opens and the player wins |
| TC07 | Repeated puzzle submission | Submit an answer for an already solved puzzle | The application must not award the same letter more than once |
| TC08 | Timer expiration | Allow the 60-second countdown to reach zero | The game displays the timeout state and prevents further progress until restarted |
| TC09 | Restart after timeout | Restart the game after the timer expires | The game resets its progress and starts a new session |

## 3. Challenging and Adversarial Situations

### Situation 1: Attempting to solve an unexamined object

A player may try to submit an answer without first examining the corresponding castle object.

**Version 1:** The validation and interaction logic are closely connected to the user interface, making independent testing more difficult.

**Version 2:** The game logic checks the examination state before accepting an answer. This prevents players from bypassing the intended puzzle interaction.

### Situation 2: Entering an incorrect answer

A player may enter random words or incorrect answers.

**Version 1:** Validation is handled within the application interface.

**Version 2:** A separate validation function checks the answer. Incorrect answers do not award letters or advance the game.

### Situation 3: Opening the final gate too early

A player may guess the final password without solving the puzzles.

**Version 1:** The initial implementation has less separation between gameplay and validation.

**Version 2:** The final gate validation checks the collected puzzle progress before allowing the player to escape.

### Situation 4: Interacting with an invalid object

A player may attempt to interact with an unknown object.

**Version 1:** Input handling is less modular and more difficult to test independently.

**Version 2:** Object validation is handled by the game logic, allowing invalid actions to be rejected safely.

### Situation 5: Timer expiration

A player may run out of time while solving the puzzles.

**Version 1:** The timer is part of the application experience.

**Version 2:** The improved application maintains a 60-second countdown and provides a restart mechanism so the player can start again.

## 4. Automated Testing

Version 2 includes automated tests using the pytest framework.

The tests are located in:

`tests/test_game_logic.py`

To execute the tests, run:

```bash
python -m pytest -v
```

The tests verify important game logic, including answer validation, object examination, puzzle completion and final gate conditions.

## 5. Test Results

The project logic test suite was previously executed successfully:

**Result: 9 tests passed.**

The automated tests help identify problems in the game logic without requiring manual gameplay for every test.

The manual scenarios listed above should also be tested through the Streamlit interface, especially the countdown and restart behaviour.

## 6. Conclusion

Testing demonstrates how Version 2 improves the reliability and maintainability of the application.

The separation of the game logic from the user interface makes it easier to test individual functions and handle incorrect player actions.

Both normal gameplay and challenging situations are considered to provide a more reliable escape-room experience.
| ID | Test | Expected result |
|---|---|---|
| T1 | Examine throne, submit THRONE | Reveal E |
| T2 | Submit incorrect answer | No letter awarded |
| T3 | Submit answer without examining object | Rejected |
| T4 | Enter ESCAPE before collecting six letters | Gate stays locked |
| T5 | Solve all six riddles and enter ESCAPE | Escape succeeds |
| T6 | Solve all riddles and enter CASTLE | Escape rejected |
| T7 | Inspect gate before collecting letters | Gate reports six missing runes |
| T8 | Examine unknown object | Rejected |
| T9 | Request a hint for each object | Hint available |

Manual adversarial checks: try blank answers, extra spaces, mixed upper/lower case, repeated object solves, and restart after partial progress.
