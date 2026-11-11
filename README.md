# Medieval Castle: The Secret Passage — Word Puzzle Escape Room

A Streamlit escape room with two versions. V1 keeps puzzle checks in the app and includes an optional Gemini castle guide. V2 moves deterministic rules into `v2_reliable/game_logic.py`.

## Story and gameplay

You are trapped in an ancient castle. Explore six objects, solve one word riddle at each, follow its letter-position instruction, and collect six letters. A parchment in the sidebar gives the order clue. Arrange the letters to form the final word and enter it at the secret stone gate.

| Object | Riddle answer | Extracted letter |
|---|---|---|
| Royal throne | THRONE | E (last) |
| Knight's shield | SWORD | S (first) |
| King's portrait | CROWN | C (first) |
| Ancient bookshelf | PASSAGE | A (second) |
| Armour stand | PLATE | P (first) |
| Treasure chest | SIEGE | E (last) |

The order clue is: monarch's seat → knight's blade → royal headwear → hidden route → knight's protection → military blockade. The letters form **ESCAPE**. Each clue requires solving a word before the letter is awarded.

## Visual design

Both V1 and V2 display the same generated medieval castle background from `assets/castle_background.jpg`, with a translucent dark overlay so the text remains readable. The interfaces also use parchment-style riddle cards and a letter inventory.

## Windows setup

```cmd
cd Locked_Room_Project
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

Run V2:
```cmd
cd v2_reliable
streamlit run app.py
```

Run V1 from the project root:
```cmd
streamlit run v1_basic/app.py
```

Optional Gemini key for the V1 guide: create `.env` in the project root with `GEMINI_API_KEY=your_key_here`. The game remains playable without it.

Run tests from the project root:
```cmd
python -m pytest -q
```

## Time limit
Both versions have a 60-second countdown. The page refreshes automatically every second. If time runs out before escape, the attempt ends and the player can restart with a fresh minute.



## Project Documentation

Additional documentation is available in the `docs/` folder:

- [Development Process](docs/development_process.md)
- [Version 1 Architecture](docs/architecture/v1_architecture.md)
- [Version 2 Architecture](docs/architecture/v2_architecture.md)
- [Test Cases](docs/test_cases.md)
- [Project Report](docs/report.md)

## Configuration

The application does not require an API key for its
core gameplay.

For the optional Gemini guide in Version 1:

1. Copy `.env.example` to `.env`.
2. Add your own Gemini API key.
3. Never upload `.env` or expose your API key on GitHub.

## Running the Application

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run Version 1:

```bash
streamlit run v1_basic/app.py
```

Run Version 2:

```bash
streamlit run v2_reliable/app.py
```

Run automated tests:

```bash
python -m pytest -q
```

