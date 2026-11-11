
# Development Process: Version 1 and Version 2

## 1. Project Overview

The project, "The Secret Passage", is a medieval castle-themed
AI Escape Room game developed using Python and Streamlit.

The player is trapped inside a castle and must solve six word
riddles. Each correct answer reveals a letter. The player must
collect all six letters, arrange them using the ordering clue,
and enter the final word ESCAPE to unlock the secret gate.

The application was developed in two versions to demonstrate
the improvement of the system.

## 2. Version 1 – Initial Prototype

### Implementation

Version 1 was developed as the initial working prototype.

It includes:
- A Streamlit-based user interface.
- A medieval castle background.
- Six interactive puzzle objects.
- Word riddles and answer validation.
- Letter collection and a final escape word.
- A 60-second countdown timer.
- An optional Gemini-powered castle guide.

### Problems encountered

1. User interface and puzzle validation were combined
   in the same application file.
2. Game logic was difficult to test independently.
3. Changes to the puzzle rules could affect the interface.
4. The code was less modular and harder to maintain.
5. The optional AI guide could provide hints, but it
   should not be responsible for validating puzzle answers.

### Why Version 2 was necessary

The initial version demonstrated the basic gameplay,
but its structure made testing and future improvements
more difficult.

A more modular design was needed to separate the
game rules from the user interface.

## 3. Version 2 – Improved and Reliable Version

### Changes introduced

Version 2 improves the internal structure of the application.

The main changes are:

1. Separated the game logic into `game_logic.py`.
2. Kept the Streamlit interface in `app.py`.
3. Added independent validation functions.
4. Added checks to prevent solving a puzzle before
   examining its object.
5. Prevented the final gate from opening before all
   six letters are collected.
6. Added automated tests using pytest.
7. Kept the 60-second countdown and restart functionality.

### Why these changes were necessary

Separating the game logic makes the application easier
to maintain, understand and test.

The Python game logic is responsible for validating
answers and controlling game progress. The Streamlit
interface is responsible for displaying the game and
collecting player input.

This separation reduces errors and makes future
features easier to implement.

## 4. Comparison Between Versions

| Feature | Version 1 | Version 2 |
|---|---|---|
| Streamlit interface | Yes | Yes |
| Castle background | Yes | Yes |
| Word puzzles | Yes | Yes |
| Countdown timer | 60 seconds | 60 seconds |
| Optional Gemini guide | Yes | Not required |
| Separate game logic module | No | Yes |
| Independent logic tests | Limited | Yes |
| Modular structure | Basic | Improved |
| Final gate validation | Embedded in app | Separate logic module |

## 5. Testing and Validation

Version 2 includes automated tests using pytest.

The tests cover:
- Correct answers.
- Incorrect answers.
- Unexamined objects.
- Unknown objects.
- Final gate validation.
- Completing all six puzzles.
- Successful escape.
- Hint functionality.

Run the tests from the project root:

```bash
python -m pytest -q
```

## 6. Conclusion

Version 1 established the main gameplay and user experience.

Version 2 improved the software architecture by separating
the user interface from the game logic and introducing
automated testing.

The second version is easier to maintain, test and extend.
