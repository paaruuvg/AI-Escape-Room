"""Deterministic word-puzzle rules for The Secret Passage (V2)."""

OBJECTS = {
    "Royal throne": {
        "icon": "👑", "answer": "THRONE", "letter": "E", "position": "last",
        "riddle": "I am a special seat raised above the hall, where a monarch sits. What am I?",
        "instruction": "Solve the word, then take its LAST letter.",
        "hint": "It begins with TH and is the name of a king's seat.",
        "success": "The throne creaks. Beneath its velvet cushion you find a letter."
    },
    "Knight's shield": {
        "icon": "🛡️", "answer": "SWORD", "letter": "S", "position": "first",
        "riddle": "I have a blade and a hilt. A knight may carry me into battle. What am I?",
        "instruction": "Solve the word, then take its FIRST letter.",
        "hint": "It is a knight's weapon; it rhymes with cord.",
        "success": "A small metal letter is engraved on the back of the shield."
    },
    "King's portrait": {
        "icon": "🖼️", "answer": "CROWN", "letter": "C", "position": "first",
        "riddle": "I rest upon a ruler's head and often shine with gold and jewels. What am I?",
        "instruction": "Solve the word, then take its FIRST letter.",
        "hint": "A king or queen wears this on their head.",
        "success": "A hidden compartment behind the portrait reveals a letter."
    },
    "Ancient bookshelf": {
        "icon": "📚", "answer": "PASSAGE", "letter": "A", "position": "second",
        "riddle": "I am a hidden route through a wall or between rooms. What am I?",
        "instruction": "Solve the word, then take its SECOND letter.",
        "hint": "It can be secret, and it leads from one place to another.",
        "success": "A loose book slides out, revealing a letter on its spine."
    },
    "Armour stand": {
        "icon": "⚔️", "answer": "PLATE", "letter": "P", "position": "first",
        "riddle": "A knight's body protection can be made from linked metal or solid ____. What word completes the phrase?",
        "instruction": "Solve the word, then take its FIRST letter.",
        "hint": "Think of the phrase '____ armour'. It is also a flat piece of metal.",
        "success": "Inside the helmet you discover a folded strip bearing a letter."
    },
    "Treasure chest": {
        "icon": "🧰", "answer": "SIEGE", "letter": "E", "position": "last",
        "riddle": "When an army surrounds a castle to force it to surrender, this is called a ____. What is the word?",
        "instruction": "Solve the word, then take its LAST letter.",
        "hint": "It begins with S and describes a military blockade around a fortress.",
        "success": "The chest opens with a groan. A final letter lies among the old coins."
    },
}

FINAL_WORD = "ESCAPE"
FINAL_ORDER = ["Royal throne", "Knight's shield", "King's portrait", "Ancient bookshelf", "Armour stand", "Treasure chest"]


def new_state():
    return {"examined": [], "solved": [], "letters": {}, "escaped": False, "messages": []}


def examine(state, item):
    if item not in OBJECTS and item != "Secret stone gate":
        return "That object is not in the castle. Choose one of the seven visible objects."
    if item not in state["examined"]:
        state["examined"].append(item)
    if item == "Secret stone gate":
        if len(state["letters"]) < len(OBJECTS):
            return "The gate has six empty runes. Find and solve all six object riddles first."
        return "The gate is ready. Arrange the six letters using the order clue and enter the hidden word."
    data = OBJECTS[item]
    if item in state["solved"]:
        return f"You already solved this clue. The letter {state['letters'][item]} is in your notebook."
    return f"{data['riddle']} {data['instruction']}"


def solve_riddle(state, item, answer):
    if item not in OBJECTS:
        return "Choose one of the six clue objects first."
    if item not in state["examined"]:
        return "Examine this object before submitting an answer."
    if item in state["solved"]:
        return f"You already solved this riddle. Your letter is {state['letters'][item]}."
    if str(answer).strip().upper() == OBJECTS[item]["answer"]:
        letter = OBJECTS[item]["letter"]
        state["solved"].append(item)
        state["letters"][item] = letter
        return f"Correct! {OBJECTS[item]['success']} You extract the letter: {letter}."
    return "That word does not fit the riddle. Think about the object and the hint."


def get_hint(item):
    if item not in OBJECTS:
        return "Examine one of the six clue objects."
    return OBJECTS[item]["hint"]


def submit_final_word(state, word):
    if len(state["letters"]) != len(OBJECTS):
        return "The gate remains sealed. You must solve all six object riddles first."
    if str(word).strip().upper() == FINAL_WORD:
        state["escaped"] = True
        return "The runes blaze: E-S-C-A-P-E. The secret passage opens. You escaped the castle!"
    return "The word is not correct. Use the parchment's order clue to arrange all six letters."
