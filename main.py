import streamlit as st
from chatbot_logic import get_chatbot_response
from database import connect_to_database
from datetime import datetime

# Page layout
st.set_page_config(page_title="Employee Helpdesk Bot", layout="wide")

# 💙 Custom CSS Styling
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton > button {
            background-color: #1e90ff;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
        }
        input::placeholder, textarea::placeholder {
            color: #4682b4 !important;
            opacity: 1 !important;
        }
        .stTextInput>div>div>input {
            border: 2px solid #1e90ff;
        }
        .css-18e3th9 {
            background-color: #e6f0ff !important;
        }
        .stApp {
            background-color: #f0f8ff;
        }
        h1 {
            color: #1e90ff !important;
        }
        .chat-bubble {
            font-size: 16px;
            padding: 10px 15px;
            margin-bottom: 10px;
            border-radius: 10px;
        }
        .user-msg {
            background-color: #ffffff;
            color: #000000;
            font-weight: 500;
        }
        .bot-msg {
            background-color: #e0ebff;
            color: #003366;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", ["💬 Chatbot", "📅 Book Room", "🛠️ Troubleshooting", "📝 Feedback"])

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "name" not in st.session_state:
    st.session_state.name = ""
if "query" not in st.session_state:
    st.session_state.query = ""

# 💬 Chatbot Page
if page == "💬 Chatbot":
    st.markdown("<h1>💬 Employee Helpdesk Chatbot</h1>", unsafe_allow_html=True)

    with st.form("chat_form"):
        st.session_state.name = st.text_input("Enter your name:", value=st.session_state.name, placeholder="Type your name here...")
        st.session_state.query = st.text_input("Ask your IT query:", value=st.session_state.query, placeholder="Eg: How to reset my email password?")
        submitted = st.form_submit_button("Submit Query")

        if submitted and st.session_state.name and st.session_state.query:
            with st.spinner("🤖 Thinking..."):
                response = get_chatbot_response(st.session_state.query)

            st.session_state.chat_history.append((st.session_state.name, st.session_state.query, "user"))
            st.session_state.chat_history.append(("Bot", response, "bot"))

            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO query_history (name, query, response) VALUES (?, ?, ?)",
                           (st.session_state.name, st.session_state.query, response))
            conn.commit()
            conn.close()

    st.subheader("Chat History")

    if st.session_state.chat_history:
        for sender, msg, role in st.session_state.chat_history:
            style_class = "bot-msg" if role == "bot" else "user-msg"
            st.markdown(
                f"<div class='chat-bubble {style_class}'><b>{sender}:</b> {msg}</div>",
                unsafe_allow_html=True
            )

        # 🧹 Clear Chat Button (clears conversation only)
        if st.button("🧹 Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []

        # 🔁 Reset for Next User (clears everything)
        if st.button("🔁 Reset for Next User", key="reset_user"):
            st.session_state.name = ""
            st.session_state.query = ""
            st.session_state.chat_history = []
            st.experimental_rerun()

# 📅 Book Room
elif page == "📅 Book Room":
    st.markdown("<h1>📅 Book a Meeting Room</h1>", unsafe_allow_html=True)

    name = st.text_input("Your Name:", placeholder="Type your name...")
    room = st.selectbox("Select Room", ["Conf A", "Conf B", "Meet X"])
    date = st.date_input("Select Date")
    time = st.time_input("Select Time")

    if st.button("Book Now"):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM room_bookings WHERE room=? AND date=? AND time=?",
                       (room, str(date), str(time)))
        existing = cursor.fetchone()

        if existing:
            st.error("Room is already booked at this time.")
        else:
            cursor.execute("INSERT INTO room_bookings (name, room, date, time, status) VALUES (?, ?, ?, ?, ?)",
                           (name, room, str(date), str(time), "Booked"))
            conn.commit()
            st.success(f"Room {room} booked successfully for {date} at {time}.")
        conn.close()

# 🛠️ Troubleshooting
elif page == "🛠️ Troubleshooting":
    st.markdown("<h1>🛠️ Common IT Issue Solutions</h1>", unsafe_allow_html=True)

    issues = {
        "Password Reset": "Go to your login screen, click on 'Forgot Password' and follow the steps.",
        "Wi-Fi Not Working": "Check router, restart your device, and ensure Airplane Mode is off.",
        "Software Installation": "Make sure you have admin rights. Download the software and follow the wizard."
    }

    selected_issue = st.selectbox("Select an Issue", list(issues.keys()))

    if selected_issue:
        st.write("### Solution:")
        st.info(issues[selected_issue])

# 📝 Feedback
elif page == "📝 Feedback":
    st.markdown("<h1>📝 Submit Feedback</h1>", unsafe_allow_html=True)

    with st.form("feedback_form"):
        name = st.text_input("Your Name:", placeholder="Enter your name")
        feedback = st.radio("Was this chatbot helpful?", ["Yes", "No"])
        comments = st.text_area("Additional Comments", placeholder="Type your suggestions or feedback here...")
        submit_feedback = st.form_submit_button("Submit Feedback")

        if submit_feedback and name:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (name, feedback) VALUES (?, ?)", (name, feedback + " - " + comments))
            conn.commit()
            conn.close()
            st.success("Thank you for your feedback!")
