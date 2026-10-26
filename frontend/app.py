import streamlit as st
import requests
import re
import html


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PrepAI - AI Interview Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user" not in st.session_state:
    st.session_state.user = None

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Java"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #fff8dc 0%,
            #fff3cd 45%,
            #fffaf0 100%
        );
    }

    .main .block-container {
        max-width: 900px;
        padding-top: 45px;
        padding-bottom: 30px;
    }

    .main-title {
        text-align: center;
        color: #a40000;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        color: #7a4a00;
        font-size: 16px;
        margin-bottom: 40px;
    }

    .section-title {
        color: #a40000;
        font-size: 20px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    div.stButton > button {
        width: 100%;
        min-height: 50px;
        background-color: white;
        color: #a40000;
        border: 2px solid #e32626;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #fff0c2;
        border-color: #b00000;
        color: #8b0000;
        transform: translateY(-2px);
        box-shadow: 0 5px 12px rgba(180, 0, 0, 0.15);
    }

    .selected-topic {
        background: #e5eee7;
        color: #1683ff;
        padding: 14px 16px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 30px;
        font-size: 16px;
    }

    .question-label {
        color: #a40000;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .answer-container {
        background: white;
        border-left: 7px solid #e32626;
        border-radius: 15px;
        padding: 22px 25px;
        margin-top: 28px;
        box-shadow: 0 5px 18px rgba(150, 50, 0, 0.12);
    }

    .answer-title {
        color: #a40000;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .answer-text {
        color: #222222;
        font-size: 16px;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding-top: 18px;
        border-top: 1px solid #e5a52b;
        color: #8a5a20;
        font-size: 13px;
    }

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GET CURRENT USER
# ============================================================

def get_current_user():

    try:

        response = requests.get(
            f"{API_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {st.session_state.access_token}"
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


# ============================================================
# GET CHAT HISTORY
# ============================================================

def get_chat_history():

    try:

        response = requests.get(
            f"{API_URL}/api/chat/history",
            headers={
                "Authorization": f"Bearer {st.session_state.access_token}"
            },
            timeout=30
        )

        if response.status_code == 200:
            return response.json()

        return []

    except Exception:
        return []


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

def clean_answer(answer):

    if not answer:
        return ""

    answer = html.unescape(answer)

    answer = re.sub(
        r"<[^>]+>",
        "",
        answer
    )

    answer = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        answer
    )

    return answer.strip()

# ============================================================
# CHAT HISTORY
# ============================================================

if st.session_state.access_token is not None:

    history = get_chat_history()

    with st.sidebar:
        st.markdown("## 💬 Chat History")

        if history:

            for item in history:

                question = item.get("question", "Unknown question")

                st.markdown(
                    f"• {question}"
                )

        else:

            st.info("No chat history yet.")


# ============================================================
# AUTHENTICATION SCREEN
# ============================================================

if st.session_state.access_token is None:

    st.markdown(
        '<div class="main-title">🤖 PREPAI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Interview Preparation Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # LOGIN / REGISTER TABS
    # ========================================================

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )


    # ========================================================
    # LOGIN TAB
    # ========================================================

    with login_tab:

        st.markdown(
            '<div class="section-title">Login to PrepAI</div>',
            unsafe_allow_html=True
        )

        login_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 LOGIN",
            use_container_width=True,
            key="login_button"
        ):

            if not login_email.strip() or not login_password:

                st.warning(
                    "⚠️ Please enter your email and password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "email": login_email,
                            "password": login_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.access_token = data[
                            "access_token"
                        ]

                        st.session_state.user = login_email

                        user_data = get_current_user()

                        if user_data:
                            st.session_state.user = user_data

                        st.success(
                            "✅ Login successful!"
                        )

                        st.rerun()

                    else:

                        try:

                            error_data = response.json()

                            error_message = error_data.get(
                                "detail",
                                "Login failed."
                            )

                        except Exception:

                            error_message = "Login failed."

                        st.error(
                            f"❌ {error_message}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Cannot connect to FastAPI backend."
                    )

                    st.info(
                        "Make sure FastAPI is running on "
                        "http://127.0.0.1:8000"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unexpected error: {str(e)}"
                    )


    # ========================================================
    # REGISTER TAB
    # ========================================================

    with register_tab:

        st.markdown(
            '<div class="section-title">'
            'Create your PrepAI account'
            '</div>',
            unsafe_allow_html=True
        )

        register_name = st.text_input(
            "Name",
            placeholder="Enter your name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        if st.button(
            "📝 CREATE ACCOUNT",
            use_container_width=True,
            key="register_button"
        ):

            if (
                not register_name.strip()
                or not register_email.strip()
                or not register_password
            ):

                st.warning(
                    "⚠️ Please fill in all fields."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "name": register_name,
                            "email": register_email,
                            "password": register_password
                        },
                        timeout=30
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.session_state.access_token = data[
                            "access_token"
                        ]

                        user_data = get_current_user()

                        if user_data:
                            st.session_state.user = user_data

                        st.success(
                            "✅ Account created successfully!"
                        )

                        st.rerun()

                    else:

                        try:

                            error_data = response.json()

                            error_message = error_data.get(
                                "detail",
                                "Registration failed."
                            )

                        except Exception:

                            error_message = "Registration failed."

                        st.error(
                            f"❌ {error_message}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "❌ Cannot connect to FastAPI backend."
                    )

                    st.info(
                        "Make sure FastAPI is running on "
                        "http://127.0.0.1:8000"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Unexpected error: {str(e)}"
                    )


    # ========================================================
    # STOP IF NOT LOGGED IN
    # ========================================================

    st.stop()


# ============================================================
# GET USER IF SESSION EXISTS
# ============================================================

if st.session_state.user is None:

    user_data = get_current_user()

    if user_data:
        st.session_state.user = user_data


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 PrepAI")

    st.markdown("---")

    # ========================================================
    # USER INFORMATION
    # ========================================================

    user = st.session_state.user

    if isinstance(user, dict):

        st.markdown(
            f"### 👤 {html.escape(user.get('name', 'User'))}"
        )

        st.caption(
            user.get("email", "")
        )

    else:

        st.markdown("### 👤 User")


    st.markdown("---")


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_button"
    ):

        st.session_state.access_token = None

        st.session_state.user = None

        st.rerun()


    st.markdown("---")


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    st.markdown("### 💬 Chat History")

    history = get_chat_history()

    if not history:

        st.info(
            "No chat history yet."
        )

    else:

        for chat in history:

            question_text = chat.get(
                "question",
                ""
            )

            answer_text = chat.get(
                "answer",
                ""
            )

            short_answer = answer_text[:100]

            if len(answer_text) > 100:

                short_answer += "..."

            st.markdown(
                f"""
                **Q:** {html.escape(question_text)}

                **A:** {html.escape(short_answer)}

                ---
                """,
                unsafe_allow_html=True
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

st.markdown(
    '<div class="main-title">'
    'AI INTERVIEW PREPARATION ASSISTANT'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Prepare smarter. Practice better. Get interview-ready with AI.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INTERVIEW TOPICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Choose your interview topic'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOPIC BUTTONS
# ============================================================

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🎯  APTITUDE",
        key="aptitude"
    ):

        st.session_state.selected_topic = "Aptitude"

with col2:

    if st.button(
        "👥  HR",
        key="hr"
    ):

        st.session_state.selected_topic = "HR"


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🌐  HTML / CSS",
        key="html_css"
    ):

        st.session_state.selected_topic = "HTML / CSS"

with col2:

    if st.button(
        "☕  JAVA",
        key="java"
    ):

        st.session_state.selected_topic = "Java"


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⚡  JAVASCRIPT",
        key="javascript"
    ):

        st.session_state.selected_topic = "JavaScript"

with col2:

    if st.button(
        "🐍  PYTHON",
        key="python"
    ):

        st.session_state.selected_topic = "Python"


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🌱  SPRING BOOT",
        key="springboot"
    ):

        st.session_state.selected_topic = "Spring Boot"

with col2:

    if st.button(
        "🗄️  SQL",
        key="sql"
    ):

        st.session_state.selected_topic = "SQL"


# ============================================================
# SELECTED TOPIC
# ============================================================

selected_topic = st.session_state.selected_topic

st.markdown(
    f"""
    <div class="selected-topic">
        Selected topic: <b>{html.escape(selected_topic)}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# QUESTION INPUT
# ============================================================

st.markdown(
    '<div class="question-label">'
    'Enter your interview question'
    '</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Question",
    placeholder=f"Ask a {selected_topic} interview question...",
    label_visibility="collapsed"
)


# ============================================================
# ASK PREPAI BUTTON
# ============================================================

ask_clicked = st.button(
    "✨  ASK PREPAI",
    use_container_width=True,
    key="ask_prepai_button"
)


# ============================================================
# SEND QUESTION TO BACKEND
# ============================================================

if ask_clicked:

    if not question.strip():

        st.warning(
            "⚠️ Please enter an interview question."
        )

    else:

        with st.spinner(
            "🤖 PrepAI is thinking..."
        ):

            try:

                # ====================================================
                # JWT AUTHORIZATION HEADER
                # ====================================================

                headers = {
                    "Authorization": (
                        f"Bearer "
                        f"{st.session_state.access_token}"
                    )
                }


                # ====================================================
                # SEND REQUEST TO FASTAPI
                # ====================================================

                response = requests.post(
                    f"{API_URL}/api/chat",
                    json={
                        "question": question
                    },
                    headers=headers,
                    timeout=120
                )


                # ====================================================
                # SUCCESS
                # ====================================================

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer was returned by the backend."
                    )

                    answer = clean_answer(answer)


                    # =================================================
                    # DISPLAY ANSWER
                    # =================================================

                    st.markdown(
                        f"""
                        <div class="answer-container">

                            <div class="answer-title">
                                🤖 PrepAI Answer
                            </div>

                            <div class="answer-text">
                                {html.escape(answer)}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ====================================================
                # UNAUTHORIZED
                # ====================================================

                elif response.status_code == 401:

                    st.error(
                        "🔐 Your login session has expired."
                    )

                    st.info(
                        "Please login again."
                    )

                    st.session_state.access_token = None

                    st.session_state.user = None

                    st.rerun()


                # ====================================================
                # BACKEND ERROR
                # ====================================================

                elif response.status_code == 500:

                    st.error(
                        "❌ Backend error: 500"
                    )

                    st.info(
                        "FastAPI received the request but "
                        "something went wrong while processing it."
                    )

                    st.info(
                        "Check the FastAPI/Uvicorn terminal "
                        "for the actual error."
                    )


                # ====================================================
                # OTHER API ERROR
                # ====================================================

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            "Unknown backend error."
                        )

                    except Exception:

                        error_message = response.text

                    st.error(
                        f"❌ Backend error: "
                        f"{response.status_code}\n\n"
                        f"{error_message}"
                    )


            # =========================================================
            # CONNECTION ERROR
            # =========================================================

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to FastAPI backend."
                )

                st.info(
                    "Please make sure Uvicorn is running on "
                    "http://127.0.0.1:8000"
                )


            # =========================================================
            # TIMEOUT
            # =========================================================

            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The backend took too long to respond."
                )

                st.info(
                    "The RAG/AI pipeline may still be processing "
                    "the request. Check the FastAPI terminal."
                )


            # =========================================================
            # OTHER ERRORS
            # =========================================================

            except Exception as e:

                st.error(
                    f"❌ Unexpected error: {str(e)}"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        © PrepAI • AI-Powered Interview Preparation Assistant

        <br>

        Practice • Learn • Improve • Succeed

    </div>
    """,
    unsafe_allow_html=True
)