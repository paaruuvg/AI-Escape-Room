import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "v2_reliable"))
from game_logic import new_state, examine, solve_riddle, submit_final_word, OBJECTS

def solved_all():
    s=new_state()
    for name, data in OBJECTS.items():
        examine(s,name); solve_riddle(s,name,data["answer"])
    return s

def test_correct_riddle_reveals_letter():
    s=new_state(); examine(s,"Royal throne")
    assert "letter: E" in solve_riddle(s,"Royal throne","throne")
    assert s["letters"]["Royal throne"]=="E"

def test_wrong_riddle_does_not_reveal_letter():
    s=new_state(); examine(s,"Royal throne")
    assert "does not fit" in solve_riddle(s,"Royal throne","king").lower()
    assert "Royal throne" not in s["letters"]

def test_must_examine_before_solving():
    s=new_state()
    assert "Examine" in solve_riddle(s,"Knight's shield","sword")

def test_cannot_skip_unfound_letters():
    s=new_state()
    assert "six object riddles" in submit_final_word(s,"ESCAPE")
    assert not s["escaped"]

def test_all_six_letters_form_escape():
    s=solved_all()
    assert [s["letters"][n] for n in OBJECTS]==list("ESCAPE")
    assert "escaped" in submit_final_word(s,"ESCAPE").lower()
    assert s["escaped"]

def test_wrong_final_word_does_not_escape():
    s=solved_all()
    assert "not correct" in submit_final_word(s,"CASTLE").lower()
    assert not s["escaped"]

def test_gate_requires_all_six_letters():
    s=new_state(); examine(s,"Secret stone gate")
    assert "six empty runes" in examine(s,"Secret stone gate")

def test_unknown_object_is_rejected():
    s=new_state()
    assert "not in the castle" in examine(s,"Dragon")

def test_hint_exists_for_each_object():
    from game_logic import get_hint
    assert all(get_hint(n) for n in OBJECTS)
