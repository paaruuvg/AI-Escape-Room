import base64
import time
from pathlib import Path
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from game_logic import OBJECTS, FINAL_ORDER, new_state, examine, solve_riddle, get_hint, submit_final_word

st.set_page_config(page_title="The Secret Passage | V2", page_icon="🏰", layout="wide")
# Refresh once per second so the 60-second countdown updates automatically.
st_autorefresh(interval=1000, key="castle_countdown_refresh")
ROOT = Path(__file__).resolve().parents[1]
img_path = ROOT / "assets" / "castle_background.jpg"
img_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8") if img_path.exists() else ""
st.markdown(f"""
<style>
.stApp {{ background: linear-gradient(rgba(12,10,12,.58),rgba(12,10,12,.72)), url('data:image/jpeg;base64,{img_b64}') center/cover fixed; }}
.block-container {{ max-width: 1250px; padding-top: 1.4rem; }}
.hero {{ background:linear-gradient(120deg,rgba(39,25,20,.96),rgba(73,43,25,.91)); border:1px solid #b58a4e; border-radius:18px; padding:1.3rem 1.6rem; box-shadow:0 10px 35px #0009; }}
.hero h1 {{ color:#f4d69a; letter-spacing:.05em; margin:0; }} .hero p {{ color:#ead9bd; margin:.3rem 0 0; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{ background:rgba(30,23,21,.88); border-color:#967346; }}
.stButton>button {{ border:1px solid #b58a4e; background:linear-gradient(120deg,#50351f,#2b211b); color:#ffedcb; border-radius:10px; font-weight:650; }}
.stButton>button:hover {{ border-color:#f4d69a; color:white; }}
div[data-testid="stForm"] {{ background:rgba(35,26,21,.92); border:1px solid #a27b47; border-radius:12px; padding:1rem; }}
h2,h3,h4 {{ color:#f4d69a !important; }}
.parchment {{ background:linear-gradient(135deg,#ead8ad,#c9aa72); color:#2b1d13; border-radius:12px; padding:1rem 1.2rem; border:3px double #79552c; }}
.parchment strong {{ color:#3b2415; }}
</style>
""", unsafe_allow_html=True)

if "game" not in st.session_state: st.session_state.game = new_state()
if "last_message" not in st.session_state: st.session_state.last_message = "The castle gate slams shut behind you. Search the chamber and recover the six letters."
if "started_at" not in st.session_state: st.session_state.started_at = time.time()
if "attempts" not in st.session_state: st.session_state.attempts = 0
if "hints_used" not in st.session_state: st.session_state.hints_used = 0
if "active_object" not in st.session_state: st.session_state.active_object = "Royal throne"
state = st.session_state.game
remaining_seconds = max(0, 60 - int(time.time() - st.session_state.started_at))
if remaining_seconds == 0 and not state["escaped"]:
    st.error("⏰ TIME IS UP! The castle gate has sealed. You have 1 minute per attempt.")
    st.warning("Your clues and progress have been reset. Try again and solve the riddles faster!")
    if st.button("🔄 Try again", type="primary", use_container_width=True):
        st.session_state.game = new_state()
        st.session_state.last_message = "A new minute begins. Search the castle and recover the six letters!"
        st.session_state.started_at = time.time()
        st.session_state.attempts = 0
        st.session_state.hints_used = 0
        st.session_state.active_object = "Royal throne"
        st.rerun()
    st.stop()

st.markdown("<div class='hero'><div style='color:#d4b47d;text-transform:uppercase;letter-spacing:.18em;font-size:.75rem'>A word-puzzle escape challenge · V2 Python-controlled</div><h1>🏰 THE SECRET PASSAGE</h1><p>Six hidden letters. Six riddles. One word stands between you and freedom.</p></div>", unsafe_allow_html=True)
solved_count = len(state["solved"])
st.progress(solved_count/6, text=f"Hidden letters recovered: {solved_count}/6")

with st.sidebar:
    remaining=max(0,60-int(time.time()-st.session_state.started_at)); m,s=divmod(remaining,60)
    st.metric("⏳ Time remaining", f"{m:02d}:{s:02d}")
    st.subheader("🎒 Letter inventory")
    for name in FINAL_ORDER:
        letter=state["letters"].get(name,"_")
        st.write(f"**{name}:** `{letter}`")
    st.divider(); st.subheader("📜 The old parchment")
    st.write("Arrange the letters in this order:")
    st.markdown("1. The monarch's seat\n2. A knight's blade\n3. What rests on a king's head\n4. A hidden route\n5. A knight's body protection\n6. A military blockade")
    st.caption(f"Wrong answers: {st.session_state.attempts} · Hints used: {st.session_state.hints_used}")
    if st.button("🔄 Restart castle", use_container_width=True):
        st.session_state.game=new_state(); st.session_state.last_message="The castle resets. Your next attempt begins now."
        st.session_state.started_at=time.time(); st.session_state.attempts=0; st.session_state.hints_used=0; st.session_state.active_object="Royal throne"; st.rerun()

st.markdown("### 🏰 Explore the castle chamber")
st.caption("Inspect the six objects. Each has a word riddle; solve it to extract one letter.")
items=list(OBJECTS.items())
cols=st.columns(3)
for i,(name,data) in enumerate(items):
    with cols[i%3]:
        with st.container(border=True):
            st.markdown(f"### {data['icon']} {name}")
            st.write("A mysterious object holds a hidden clue.")
            if name in state["solved"]: st.success(f"Letter found: {state['letters'][name]}")
            elif name in state["examined"]: st.caption("Riddle discovered · waiting for your answer")
            if st.button(f"🔍 Examine {name}", key=f"ex_{i}", use_container_width=True):
                st.session_state.active_object=name
                st.session_state.last_message=examine(state,name); st.rerun()
with st.container(border=True):
    st.markdown("### 🚪 Secret stone gate")
    st.write("The final gate has six empty runes. It will accept only the hidden word.")
    if st.button("Inspect the secret gate", key="gate_inspect"):
        st.session_state.last_message=examine(state,"Secret stone gate"); st.rerun()

st.markdown("### 🔎 Solve the selected object's riddle")
active=st.session_state.active_object
if active in OBJECTS:
    data=OBJECTS[active]
    st.markdown(f"<div class='parchment'><strong>{data['icon']} {active}</strong><br><br>{data['riddle']}<br><em>{data['instruction']}</em></div>",unsafe_allow_html=True)
    if active in state["solved"]:
        st.success(f"You recovered **{state['letters'][active]}** from this object.")
    else:
        with st.form("answer_form", clear_on_submit=True):
            answer=st.text_input("Your answer (one word)", placeholder="Type the word you think solves the riddle")
            submitted=st.form_submit_button("Unlock hidden letter",use_container_width=True)
        if submitted:
            response=solve_riddle(state,active,answer)
            if response.startswith("That word"): st.session_state.attempts+=1
            st.session_state.last_message=response; st.rerun()
        if st.button("💡 Ask for a hint",key="hint_"+active):
            st.session_state.hints_used+=1; st.session_state.last_message=get_hint(active); st.rerun()
else:
    st.info("Choose an object above to investigate its riddle.")

st.info(st.session_state.last_message,icon="📜")
st.markdown("### 🧩 Final challenge — discover the secret word")
st.write("Once all six letters are found, arrange them using the old parchment in the sidebar. The order of discovery does not matter.")
with st.form("final_form"):
    final_word=st.text_input("Enter the six-letter secret word",max_chars=12,placeholder="_ _ _ _ _ _")
    final_submit=st.form_submit_button("Open the secret passage",use_container_width=True)
if final_submit:
    response=submit_final_word(state,final_word)
    if "not correct" in response: st.session_state.attempts+=1
    st.session_state.last_message=response; st.rerun()
if state["escaped"]:
    st.balloons(); st.success("🏆 YOU ESCAPED! The six runes blaze, the hidden wall opens, and moonlight floods the passage.")
    st.write(f"Wrong answers: **{st.session_state.attempts}** · Hints used: **{st.session_state.hints_used}**")
    if st.button("Play again",type="primary"):
        st.session_state.game=new_state(); st.session_state.started_at=time.time(); st.session_state.attempts=0; st.session_state.hints_used=0; st.session_state.active_object="Royal throne"; st.rerun()
