# Test cases — Word Puzzle Version

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
