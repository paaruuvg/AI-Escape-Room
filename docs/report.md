# Project report — The Secret Passage

## Overview
The player is trapped in a medieval castle and must solve six word riddles. Each correct answer reveals one letter according to a letter-position instruction. A parchment provides a semantic ordering clue; the six letters form the final word ESCAPE. The player enters that word at the secret stone gate.

## V1 and its limitations
V1 is an LLM-assisted prototype. Streamlit displays the objects and riddles, while the puzzle validation and session-state updates are embedded directly in `v1_basic/app.py`. An optional Gemini castle guide answers general help questions, with a fixed fallback if no key is configured. Keeping UI and game rules together makes the code harder to test and maintain.

## V2 improvements
V2 separates deterministic rules into `v2_reliable/game_logic.py`. The module validates object examination, riddle answers, letter extraction, final-word prerequisites and escape state. The interface handles display and input. Invalid or premature actions do not reveal letters or open the gate. This improves reliability, modularity and testability.

## Architecture
**V1:** Player → Streamlit UI (objects, forms, session state and embedded validation) ↔ optional Gemini guide / offline hint.

**V2:** Player → Streamlit UI (`app.py`) → Python game logic (`game_logic.py`) → validated state (examined objects, solved riddles, letters, escaped) → UI feedback and notebook.

## Puzzle sequence
Throne/THRONE→E; shield/SWORD→S; portrait/CROWN→C; bookshelf/PASSAGE→A; armour/PLATE→P; chest/SIEGE→E. The order clue identifies the correct semantic sequence. The final word is ESCAPE.

## Testing
The V2 test suite covers correct and incorrect riddle answers, prerequisite enforcement, final-word gating, full escape, unknown objects and hints. Run `python -m pytest -q` from the project root. For the class demonstration, also show blank and malformed answers, repeated submissions, and restarting after partial progress.

## Limitations
The riddles and final word are fixed, so replayability is limited. The optional LLM is only a guide; Python validates all puzzle progress. Streamlit session state provides memory for the current play session and resets on restart.
