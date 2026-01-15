import streamlit as st
import pandas as pd
import extra_streamlit_components as stx
import json
import time

# Set page config
st.set_page_config(layout="wide", page_title="Masterclass - Sovereign Console", page_icon="logo.png")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- COOKIE MANAGER ---
@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# --- DATA ---
COURSE_CONTENT = {
    "Module 1: The Shield (Survival, Safety & Psychology)": [
        "Lesson 1: The 70-Year AI Rollercoaster – Origins to Explosion",
        "Lesson 2: Digital Self-Defense & Data Hygiene",
        "Lesson 3: Psychological Firewalls (Mental Health & Guardrails)"
    ],
    "Module 2: The Creator (Content, Visuals & Strategy)": [
        "Lesson 4: The Vanguard Toolbox (Commanding the Essentials)",
        "Lesson 5: High-Level Prompt Engineering (The Context Pathway)",
        "Lesson 6: Visual Dominance: Hybrid AI & The Premium Stock Hack",
        "Lesson 7: The \"Faceless\" Growth Strategy",
        "Lesson 8: Generative Engine Optimization (GEO)"
    ],
    "Module 3: The Operator (AI Automation, Agents & Builders)": [
        "Lesson 9: The \"Agentic\" Revolution (The Foundation)",
        "Lesson 10: Media & Content Automation (Replacing the Creative Team)",
        "Lesson 11: Building \"Digital Employees\" (Business & Sales)",
        "Lesson 12: Infrastructure, Cost & Privacy",
        "Lesson 13: The Sovereign Mind (Fine-Tuning & Localization)",
        "Lesson 14: Computer Vision (The Eyes of AI)",
        "Lesson 15: The Certified Vanguard (Free Education & Badges)",
        "Lesson 16: The Vibe Coder (Building Custom Apps)"
    ]
}

# Flatten content
FLATTENED_LESSONS = []
for module, lessons in COURSE_CONTENT.items():
    for lesson in lessons:
        FLATTENED_LESSONS.append({"module": module, "title": lesson})

# --- STATE SYNC ---
# Try load from cookies if session state is empty
cookies = cookie_manager.get_all()

if 'current_lesson_index' not in st.session_state:
    saved_index = cookies.get('current_lesson_index')
    st.session_state.current_lesson_index = int(saved_index) if saved_index else 0

if 'completed_lessons' not in st.session_state:
    saved_completed = cookies.get('completed_lessons')
    if saved_completed:
        try:
            st.session_state.completed_lessons = set(json.loads(saved_completed))
        except:
             st.session_state.completed_lessons = set()
    else:
        st.session_state.completed_lessons = set()

# --- NAVIGATION FUNCTIONS ---
def save_state():
    cookie_manager.set('current_lesson_index', st.session_state.current_lesson_index, key="set_idx")
    # Convert set to list for JSON serialization
    completed_list = list(st.session_state.completed_lessons)
    cookie_manager.set('completed_lessons', json.dumps(completed_list), key="set_completed")

def next_lesson():
    if st.session_state.current_lesson_index < len(FLATTENED_LESSONS) - 1:
        st.session_state.current_lesson_index += 1
        save_state()

def prev_lesson():
    if st.session_state.current_lesson_index > 0:
        st.session_state.current_lesson_index -= 1
        save_state()

def complete_lesson():
    st.session_state.completed_lessons.add(st.session_state.current_lesson_index)
    save_state()
    # Force reload to update cookies visually if needed (stx sometimes needs it)
    # time.sleep(0.1) 

def jump_to_lesson(idx):
    st.session_state.current_lesson_index = idx
    save_state()

# --- CONTENT DATA ---
# UPDATE THIS SECTION WITH YOUR ACTUAL LINKS
LESSON_DETAILS = {
    "Lesson 1: The 70-Year AI Rollercoaster – Origins to Explosion": {
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Replace with actual URL
        "slides": "#", # Replace with PDF link or delete if none
        "desc": "Understanding the history of AI."
    },
    "Lesson 2: Digital Self-Defense & Data Hygiene": {
        "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
        "slides": "#"
    },
    # Add more lessons here as needed...
}

# --- UI LAYOUT ---
# Create two columns to mimic the "Card" layout
left_col, right_col = st.columns([1, 2], gap="large")

current_lesson = FLATTENED_LESSONS[st.session_state.current_lesson_index]
progress_pct = len(st.session_state.completed_lessons) / len(FLATTENED_LESSONS)

with left_col:
    st.markdown("### Profile")
    # Logo
    st.image("logo.png", width=100)
    st.markdown("### Reignit, AI Vanguard")
    
    # Navigation Buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Previous"):
            prev_lesson()
            st.rerun()
    with c2:
        if st.button("Next"):
            next_lesson()
            st.rerun()
            
    # Progress
    st.markdown(f"**Progress: {int(progress_pct * 100)}%**")
    st.progress(progress_pct)
    
    st.markdown("---")
    
    # Course Outline (Display modules and highlight active lesson)
    for module, lessons in COURSE_CONTENT.items():
        st.markdown(f"**{module}**")
        for lesson in lessons:
            # Check if this is the current lesson
            is_active = lesson == current_lesson['title']
            marker = "🔵" if is_active else "⚪"
            # check completed
            lesson_idx = next((i for i, item in enumerate(FLATTENED_LESSONS) if item["title"] == lesson), -1)
            if lesson_idx in st.session_state.completed_lessons:
                marker = "✅"
            
            style_class = "nav-active" if is_active else "nav-item"
            
            # Since we can't easily make clickable div text trigger state changes without components,
            # For this prototype, we'll just display the list. 
            # Ideally, these would be buttons or clickable links using a component like streamlit-aggrid or just buttons.
            # Using buttons with custom key to avoid duplicates
            if st.button(f"{marker} {lesson.split(': ')[0]}", key=lesson, help=lesson,  use_container_width=True):
                 jump_to_lesson(lesson_idx)
                 st.rerun()

with right_col:
    st.markdown(f"## {current_lesson['module']}")
    st.markdown(f"# {current_lesson['title']}")
    
    # Get details for this lesson
    details = LESSON_DETAILS.get(current_lesson['title'], {})
    video_url = details.get("video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Default fallback
    slides_url = details.get("slides", "#")
    description = details.get("desc", "")

    # Video Player
    st.video(video_url)
    
    if description:
        st.markdown(description)
    
    st.markdown("### Lesson Resources")
    if slides_url != "#":
        st.markdown(f"- [📥 Download Slides / Resources]({slides_url})")
    else:
        st.markdown("_No resources attached for this lesson._")
    
    st.markdown("---")

    if st.button("✅ Mark as Complete", key="complete_btn"):
        complete_lesson()
        st.success("Lesson Marked as Complete!")
        st.rerun()

