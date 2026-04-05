import streamlit as st
import json

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "Listening to music helps me concentrate better while studying.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music reduces distractions from my surroundings during study sessions.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "I find it easier to stay focused on tasks when music is playing.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Certain types of music improve my ability to understand complex material.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "I complete study tasks faster when listening to music.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music helps me maintain a steady study pace.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "I feel more productive when I study with music compared to silence.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Background music increases my motivation to start studying.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Instrumental music (no lyrics) improves my focus more than music with lyrics.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music with lyrics distracts me from reading or writing tasks.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "I choose different types of music depending on the difficulty of the task.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music helps reduce stress during study sessions.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Listening to music improves my mood while studying.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music helps me stay engaged for longer periods without feeling tired.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]},

    {"q": "Music sometimes distracts me and reduces my study performance.",
     "opts": [("Never", 0), ("Rarely", 1), ("Sometimes", 2), ("Often", 3), ("Always", 4)]}
]

psych_states = {
    "Low Influence of Music": (0, 15),
    "Slight Positive Influence": (16, 30),
    "Moderate Influence on Focus & Productivity": (31, 45),
    "Strong Positive Influence": (46, 55),
    "High Dependence on Music": (56, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(char.isdigit() for char in name)

def validate_student_id(student_id: str) -> bool:
    return student_id.isdigit() and len(student_id.strip()) > 0

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Student Music Study Survey", page_icon="📝")
st.title("📝 Student Music Study Survey")
st.write("Please fill out your details and answer all questions honestly.")

# ---------------- FORM ----------------
with st.form("survey_form"):
    st.subheader("Student Information")
    name = st.text_input("Given Name")
    surname = st.text_input("Surname")
    dob = st.date_input("Date of Birth")
    sid = st.text_input("Student ID (digits only)")

    st.subheader("Survey Questions")

    answers = []
    total_score = 0

    for idx, q in enumerate(questions):
        option_labels = [label for label, score in q["opts"]]
        selected_option = st.radio(
            f"Q{idx + 1}. {q['q']}",
            option_labels,
            key=f"q_{idx}"
        )

        selected_score = next(
            score for label, score in q["opts"] if label == selected_option
        )

        total_score += selected_score
        answers.append({
            "question": q["q"],
            "selected_option": selected_option,
            "score": selected_score
        })

    submitted = st.form_submit_button("Submit Survey")

# ---------------- RESULT ----------------
if submitted:
    errors = []

    if not validate_name(name):
        errors.append("Please enter a valid given name.")
    if not validate_name(surname):
        errors.append("Please enter a valid surname.")
    if not validate_student_id(sid):
        errors.append("Student ID must contain digits only.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        result_status = interpret_score(total_score)

        record = {
            "name": name.strip(),
            "surname": surname.strip(),
            "dob": str(dob),
            "student_id": sid.strip(),
            "total_score": total_score,
            "result": result_status,
            "answers": answers,
            "version": version_float
        }

        json_data = json.dumps(record, indent=2)
        file_name = f"{sid.strip()}_result.json"

        st.success("Survey submitted successfully.")
        st.markdown(f"### Result: {result_status}")
        st.markdown(f"**Total Score:** {total_score}")

        st.download_button(
            label="Download Result as JSON",
            data=json_data,
            file_name=file_name,
            mime="application/json"
        )