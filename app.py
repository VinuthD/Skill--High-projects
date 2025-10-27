import streamlit as st
import time



try:
    from transformers import pipeline
    import torch
    device = 0 if torch.cuda.is_available() else -1
    qa_pipeline = pipeline(
        "question-answering",
        model="distilbert-base-cased-distilled-squad",
        device=device
    )
except Exception:
    st.warning(" Running without QA model (using fallback responses).")
    def qa_pipeline(input_dict):
        return {"answer": "I'm sorry, I can’t answer that specifically, but I can help with SkillHigh course or platform info!"}

course_categories = {
    "technology & programming": {
        "1": "AI & ML (Artificial Intelligence & Machine Learning): Foundational concepts, advanced techniques, and practical applications.",
        "2": "Data Science: Data analysis, visualization, predictive modeling, and machine learning using Python, R, and relevant libraries.",
        "3": "Data Structures and Algorithms: Core concepts for efficient problem-solving and software optimization.",
        "4": "Full Stack Web Development: Mastering front-end (React) and back-end (Node.js, Express, MongoDB, SQL) development.",
        "5": "App Development: Designing, building, and deploying mobile applications for Android and iOS.",
        "6": "Cloud Computing: Fundamentals of AWS, Azure, and Google Cloud, including EC2, S3, and Kubernetes.",
        "7": "IoT (Internet of Things): Building IoT systems with sensors, communication, and analytics.",
        "0": "Back to Main Menu"
    },
    "business & analytics": {
        "1": "Data Analytics: Extracting insights using Excel, Tableau, Power BI, and SQL.",
        "2": "Business Analytics: Using data for better business decisions and predictive analytics.",
        "3": "Digital Marketing: SEO, SEM, content marketing, social media, and email campaigns.",
        "4": "Human Resources: Recruitment, talent management, employee relations, and performance management.",
        "5": "Finance: Financial analysis, investment strategies, corporate finance, and modeling.",
        "6": "Cyber Security: Protecting systems and networks, ethical hacking, encryption, and security protocols.",
        "0": "Back to Main Menu"
    }
}

faq_data = {
    "internship": "Skill High (or Skillintern) is an online training and internship platform.It offers short online courses with live and recorded classes.After training, students work on live projects for practical experience.",
    "certificate": "SkillHigh provides course completion certificates upon successfully finishing each program.",
    "onboarding": "You can register on our website or contact our support team for onboarding assistance.",
    "contact": "You can reach us at support@skillhigh.in.",
    "about": "SkillHigh is an online learning platform providing practical, job-ready training in technology, analytics, and business fields."
}

small_talk = {
    "hi": "Hello there  How can I help you today?",
    "hello": "Hi! Welcome to SkillHigh. Would you like to know about our courses or certificates?",
    "hey": "Hey! How’s it going? Want to explore some SkillHigh courses?",
    "how are you": "I’m doing great, thanks for asking!  How can I assist you today?",
    "good morning": "Good morning!  Ready to learn something new today?",
    "good afternoon": "Good afternoon!  What would you like to explore?",
    "good evening": "Good evening!  Would you like to check out our latest courses?",
    "thanks": "You’re very welcome! ",
    "thank you": "Always happy to help! ",
    "bye": "Goodbye  Have a great day learning with SkillHigh!"
}




def get_intent(query):
    query = query.lower()
    if query in small_talk:
        return "small_talk"
    elif "course" in query or "learn" in query or "offer" in query:
        return "course"
    elif "internship" in query:
        return "internship"
    elif "join" in query or "onboard" in query:
        return "onboarding"
    elif "contact" in query or "support" in query:
        return "contact"
    elif "certificate" in query:
        return "certificate"
    elif "about" in query:
        return "about"
    else:
        return "general"

st.set_page_config(page_title="SkillHigh Chatbot", layout="wide")

st.markdown("""
<style>
body {background-color:#0d0f13; color:white;}
h2 {color:white; text-align:center;}
.user {
    background-color:#0078ff;
    color:white;
    padding:10px 15px;
    border-radius:15px;
    max-width:60%;
    margin-left:auto;
    margin-top:10px;
}
.bot {
    background-color:#202225;
    color:white;
    padding:10px 15px;
    border-radius:15px;
    max-width:60%;
    margin-right:auto;
    margin-top:10px;
}
.stTextInput>div>div>input {
    background-color:#1e1f23;
    color:white;
    border:1px solid #333;
    border-radius:8px;
    padding:10px;
}
.stTextInput>div>label {color:#a8a8a8!important;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2> SkillHigh Assistant</h2>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("bot", " Welcome to SkillHigh! I’m your AI learning assistant."),
        ("bot", "You can ask me about our courses, certificates, internships, or anything about SkillHigh!")
    ]
    
    
    
    
if "typing" not in st.session_state:
    st.session_state.typing = False
if "awaiting_category" not in st.session_state:
    st.session_state.awaiting_category = False
if "awaiting_course" not in st.session_state:
    st.session_state.awaiting_course = None

for sender, msg in st.session_state.chat_history:
    role_class = "user" if sender == "user" else "bot"
    st.markdown(f"<div class='{role_class}'>{msg}</div>", unsafe_allow_html=True)

if st.session_state.typing:
    st.markdown("<div class='bot'>SkillBot is typing...</div>", unsafe_allow_html=True)





with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:")
    send_btn = st.form_submit_button("Send")





if send_btn and user_input.strip():
    msg = user_input.strip()
    st.session_state.chat_history.append(("user", msg))

    if st.session_state.awaiting_course:
        category = st.session_state.awaiting_course
        if msg == "0" or "back" in msg.lower():
            st.session_state.awaiting_course = None
            answer = "Back to main menu  You can ask about: Courses, Certificates, Internships, or About SkillHigh."
        elif msg in course_categories[category]:
            if msg != "0":
                answer = course_categories[category][msg]
                st.session_state.awaiting_course = None
            else:
                st.session_state.awaiting_course = None
                answer = "Returning to main menu. You can now ask another question."
        else:
            options = "\n".join([f"{num}. {desc.split(':')[0]}" for num, desc in course_categories[category].items()])
            answer = f"I didn’t catch that. Please select a valid course number:\n{options}"

    elif st.session_state.awaiting_category:
        choice = msg.strip()
        if choice == "1" or "technology" in choice.lower():
            st.session_state.awaiting_course = "technology & programming"
            st.session_state.awaiting_category = False
            options = "\n".join([f"{num}. {desc.split(':')[0]}" for num, desc in course_categories["technology & programming"].items()])
            answer = f"Here are the available courses:\n{options}\n\nType the course number to know more (or 0 to go back)."
        elif choice == "2" or "business" in choice.lower():
            st.session_state.awaiting_course = "business & analytics"
            st.session_state.awaiting_category = False
            options = "\n".join([f"{num}. {desc.split(':')[0]}" for num, desc in course_categories["business & analytics"].items()])
            answer = f"Here are the available courses:\n{options}\n\nType the course number to know more (or 0 to go back)."
        else:
            answer = "Please reply with '1' for Technology & Programming or '2' for Business & Analytics."

    else:
        intent = get_intent(msg)
        if intent == "small_talk":
            answer = small_talk[msg.lower()]
        elif intent == "course":
            answer = "We offer courses in two main categories:\n1. Technology & Programming\n2. Business & Analytics\nPlease reply with the number (1 or 2) of the category you'd like to explore."
            st.session_state.awaiting_category = True
        elif intent in faq_data:
            answer = faq_data[intent]
        else:
            qa_result = qa_pipeline({
                'context': "SkillHigh is an AI learning platform offering various programs in technology, analytics, and business.",
                'question': msg
            })
            answer = qa_result['answer']



    st.session_state.chat_history.append(("bot", answer))
    st.session_state.typing = False
    st.rerun()
