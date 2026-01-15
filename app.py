import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(layout="wide", page_title="Masterclass - Sovereign Console", page_icon="🎓")

# Load Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

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

# Flatten content for easier navigation
FLATTENED_LESSONS = []
for module, lessons in COURSE_CONTENT.items():
    for lesson in lessons:
        FLATTENED_LESSONS.append({"module": module, "title": lesson})

# --- SESSION STATE ---
if 'current_lesson_index' not in st.session_state:
    st.session_state.current_lesson_index = 0

if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = set()

# --- NAVIGATION FUNCTIONS ---
def next_lesson():
    if st.session_state.current_lesson_index < len(FLATTENED_LESSONS) - 1:
        st.session_state.current_lesson_index += 1

def prev_lesson():
    if st.session_state.current_lesson_index > 0:
        st.session_state.current_lesson_index -= 1

def complete_lesson():
    st.session_state.completed_lessons.add(st.session_state.current_lesson_index)

# --- UI LAYOUT ---
# Create two columns to mimic the "Card" layout
left_col, right_col = st.columns([1, 2], gap="large")

current_lesson = FLATTENED_LESSONS[st.session_state.current_lesson_index]
progress_pct = len(st.session_state.completed_lessons) / len(FLATTENED_LESSONS)

with left_col:
    st.markdown("### Profile")
    # Placeholder Avatar
    st.markdown("""
    <div style="text-align: center;">
        <div style="width: 80px; height: 80px; background-color: #ddd; border-radius: 50%; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; font-size: 24px;">👤</div>
        <h3>Reignit User</h3>
    </div>
    """, unsafe_allow_html=True)
    
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
                 st.session_state.current_lesson_index = lesson_idx
                 st.rerun()

with right_col:
    st.markdown(f"## {current_lesson['module']}")
    st.markdown(f"# {current_lesson['title']}")
    
    # Video Placeholder
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Rick roll placeholder - PLEASE REPLACE
    
    st.info("ℹ️ This is a placeholder video. Please replace with actual course content.")
    
    st.markdown("### Lesson Resources")
    st.markdown("- [Slide Deck (PDF)](#)")
    st.markdown("- [Reference Link](#)")
    
    if st.button("✅ Mark as Complete", key="complete_btn"):
        complete_lesson()
        st.success("Lesson Marked as Complete!")
        st.rerun()

