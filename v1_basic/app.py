import os, time, base64
from pathlib import Path
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv
load_dotenv()
st.set_page_config(page_title="The Secret Passage | V1", page_icon="🏰", layout="wide")
# Refresh once per second so the 60-second countdown updates automatically.
st_autorefresh(interval=1000, key="castle_countdown_refresh_v1")
ROOT = Path(__file__).resolve().parents[1]
img_path = ROOT / "assets" / "castle_background.jpg"
img_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8") if img_path.exists() else ""
st.markdown(f"""
<style>
.stApp {{ background: linear-gradient(rgba(12,10,12,.58),rgba(12,10,12,.72)), url('data:image/jpeg;base64,{img_b64}') center/cover fixed; }}
.block-container {{ max-width: 1250px; padding-top: 1.4rem; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background: rgba(30,23,21,.86); border: 1px solid #967346; border-radius: 12px; }}
.stButton>button {{ border: 1px solid #b58a4e; background: linear-gradient(120deg,#50351f,#2b211b); color: #ffedcb; border-radius: 10px; font-weight: 650; }}
.stButton>button:hover {{ border-color: #f4d69a; color: white; }}
h1,h2,h3,h4 {{ color: #f4d69a; }}
</style>
""", unsafe_allow_html=True)
OBJECTS = {
 "Royal throne":("👑","I am a special seat raised above the hall, where a monarch sits. What am I? Take its LAST letter.","THRONE","E","The throne creaks; beneath its velvet cushion is a letter."),
 "Knight's shield":("🛡️","I have a blade and a hilt. A knight may carry me into battle. What am I? Take its FIRST letter.","SWORD","S","A small metal letter is engraved on the back of the shield."),
 "King's portrait":("🖼️","I rest upon a ruler's head and often shine with gold and jewels. What am I? Take its FIRST letter.","CROWN","C","A hidden compartment behind the portrait reveals a letter."),
 "Ancient bookshelf":("📚","I am a hidden route through a wall or between rooms. What am I? Take my SECOND letter.","PASSAGE","A","A loose book slides out, revealing a letter on its spine."),
 "Armour stand":("⚔️","A knight's body protection can be made from linked metal or solid ____. What word completes the phrase? Take its FIRST letter.","PLATE","P","Inside the helmet you discover a folded strip bearing a letter."),
 "Treasure chest":("🧰","When an army surrounds a castle to force it to surrender, this is called a ____. Take its LAST letter.","SIEGE","E","The chest opens with a groan; a final letter lies among the old coins.")
}
if "solved" not in st.session_state: st.session_state.solved=[]
if "letters" not in st.session_state: st.session_state.letters={}
if "history" not in st.session_state: st.session_state.history=[]
if "active" not in st.session_state: st.session_state.active="Royal throne"
if "escaped" not in st.session_state: st.session_state.escaped=False
if "attempts" not in st.session_state: st.session_state.attempts=0
if "started_at" not in st.session_state: st.session_state.started_at=time.time()
remaining_seconds=max(0,60-int(time.time()-st.session_state.started_at))
if remaining_seconds == 0 and not st.session_state.escaped:
 st.error("⏰ TIME IS UP! The castle gate has sealed. You have 1 minute per attempt.")
 st.warning("Your clues and progress have been reset. Try again and solve the riddles faster!")
 if st.button("🔄 Try again",type="primary"):
  for k in ["solved","letters","history","active","escaped","attempts"]: st.session_state.pop(k,None)
  st.session_state.started_at=time.time()
  st.rerun()
 st.stop()
st.title("🏰 THE SECRET PASSAGE")
st.caption("Medieval Castle Word Escape Room · V1 — LLM-assisted guide; puzzle checks are embedded in this app")
st.write("The castle gate slams shut behind you. Solve six word riddles, extract one letter from each object, arrange the letters and escape.")
st.progress(len(st.session_state.solved)/6,text=f"Letters recovered: {len(st.session_state.solved)}/6")
with st.sidebar:
 remaining=max(0,60-int(time.time()-st.session_state.started_at)); mm,ss=divmod(remaining,60)
 st.metric("⏳ Time remaining",f"{mm:02d}:{ss:02d}")
 st.subheader("📜 Letter notebook")
 for n in OBJECTS: st.write(f"{n}: `{st.session_state.letters.get(n,'_')}`")
 st.subheader("Order clue")
 st.write("Seat → weapon → royal headwear → hidden route → knight's protection → siege")
 if st.button("Restart castle"):
  for k in ["solved","letters","history","active","escaped","attempts"]: st.session_state.pop(k,None)
  st.session_state.started_at=time.time()
  st.rerun()
st.subheader("Explore the chamber")
cols=st.columns(3)
for i,(name,data) in enumerate(OBJECTS.items()):
 with cols[i%3]:
  with st.container(border=True):
   st.markdown(f"### {data[0]} {name}")
   if name in st.session_state.solved: st.success("Letter: "+st.session_state.letters[name])
   if st.button("Examine",key=f"obj{i}"):
    st.session_state.active=name; st.rerun()
name=st.session_state.active; data=OBJECTS[name]
st.markdown(f"### 🧩 {name}")
st.info(data[1])
if name not in st.session_state.solved:
 answer=st.text_input("Your one-word answer",key="answer_"+name)
 if st.button("Reveal the letter",key="solve_"+name):
  if answer.strip().upper()==data[2]:
   # V1 directly updates session state inside the UI file.
   letter=data[3]; st.session_state.solved.append(name); st.session_state.letters[name]=letter
   st.session_state.history.append(data[4]+" Letter: "+letter); st.success(data[4]+" Letter: "+letter); st.rerun()
  else:
   st.session_state.attempts+=1; st.error("Not quite. Think about the riddle and the extraction instruction.")
 if st.button("Show a gentle hint",key="hint_"+name):
  hints={"Royal throne":"It begins with TH; a king sits on it.","Knight's shield":"A knight's blade weapon.","King's portrait":"A ruler wears it on their head.","Ancient bookshelf":"A secret route through a building.","Armour stand":"Think of the phrase '____ armour'.","Treasure chest":"A military blockade around a castle."}
  st.info(hints[name])
else: st.success("Already solved. Letter: "+st.session_state.letters[name])
st.divider(); st.subheader("🚪 Final challenge — assemble the hidden word")
st.write("Use the order clue in the sidebar. The letters should form a word meaning to break free.")
word=st.text_input("Enter the six-letter word",max_chars=12)
if st.button("Open secret passage"):
 if len(st.session_state.letters)<6: st.warning("Find all six letters first.")
 elif word.strip().upper()=="ESCAPE": st.session_state.escaped=True; st.balloons(); st.success("The passage opens. You escaped the castle!")
 else: st.session_state.attempts+=1; st.error("That is not the hidden word. Check the order clue.")
if st.session_state.escaped: st.balloons(); st.success("🏆 YOU ESCAPED THE CASTLE!")
st.caption(f"Incorrect attempts: {st.session_state.attempts}")
st.subheader("Ask the castle guide")
question=st.text_input("Ask for help",placeholder="What should I look for?")
if st.button("Ask guide") and question.strip():
 answer_text="Start with the throne. Solve each object's riddle, then follow the letter-position instruction. The parchment order clue helps assemble the final word."
 api_key=os.getenv("GEMINI_API_KEY")
 if api_key:
  try:
   import google.generativeai as genai
   genai.configure(api_key=api_key)
   model=genai.GenerativeModel("gemini-1.5-flash")
   answer_text=model.generate_content("You are a medieval castle guide. Give a small hint but never reveal the final answer. The game has six riddles. Player asks: "+question).text
  except Exception: pass
 st.info(answer_text)
