from pypdf import PdfReader
import streamlit as st
import database
from ai_helper import ask_gemini
import io
import json
import speech_recognition as sr
import streamlit.components.v1 as components
from streamlit_mic_recorder import speech_to_text
# Initialize database
database.create_database()

# Configure website
st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Agent")
st.caption("Your personal assistant for placement preparation.")

# Initialize session state
if "solved_questions" not in st.session_state:
    st.session_state.solved_questions = []

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"
def extract_resume_text(uploaded_file):
    """Extract readable text from an uploaded PDF or TXT resume."""

    if uploaded_file.name.lower().endswith(".pdf"):
        pdf_reader = PdfReader(uploaded_file)
        pages_text = []

        for page in pdf_reader.pages:
            pages_text.append(page.extract_text() or "")

        return "\n".join(pages_text)

    return uploaded_file.getvalue().decode("utf-8", errors="replace")
# Navigation

pages = [
    "Dashboard",
    "DSA Practice",
    "AI Recommendations",
    "Study Plan",
    "AI Career Chat",
    "AI Resume Analyzer",
    "AI Mock Interview"
]

st.markdown("""
<style>
    /* Main application background */
    .stApp {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #faf5ff 55%,
            #fdf2f8 100%
        );
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #312e81 0%,
            #4338ca 55%,
            #6d28d9 100%
        );
    }

    
/* Keep sidebar labels readable */
[data-testid="stSidebar"] {
    color: #ffffff;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

/* Navigation options: dark text on light backgrounds */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="listbox"] {
    color: #312e81 !important;
}
4

    /* Main headings */
    h1, h2, h3 {
        color: #4338ca;
        font-weight: 700;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #e9d5ff;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(67, 56, 202, 0.08);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(
            90deg,
            #4338ca,
            #db2777
        );
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border: 1px solid #db2777;
        color: white;
        box-shadow: 0 4px 14px rgba(219, 39, 119, 0.25);
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 10px;
    }

    /* Dividers */
    hr {
        border-color: #e9d5ff;
    }
</style>
""", unsafe_allow_html=True)


st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Choose a section",
    pages,
    index=pages.index(st.session_state.selected_page)
)

st.session_state.selected_page = page

# DSA question bank
questions = {
    "Arrays": [
        {
            "id": "array_1",
            "title": "Find the largest element",
            "difficulty": "Easy",
            "question": "Given the list [4, 9, 2, 7, 5], what is the largest element?",
            "answer": "9",
            "hint": "Compare the elements and keep track of the largest one.",
            "explanation": "9 is greater than every other element in the list."
        },
        {
            "id": "array_2",
            "title": "Sum of array elements",
            "difficulty": "Easy",
            "question": "What is the sum of [2, 4, 6, 8]?",
            "answer": "20",
            "hint": "Add all four elements.",
            "explanation": "2 + 4 + 6 + 8 = 20."
        }
    ],
    "Strings": [
        {
            "id": "string_1",
            "title": "Reverse a string",
            "difficulty": "Easy",
            "question": "What is the reverse of the string 'python'?",
            "answer": "nohtyp",
            "hint": "Read the characters from right to left.",
            "explanation": "Reversing python gives nohtyp."
        }
    ],
    "Basic Mathematics": [
        {
            "id": "math_1",
            "title": "Check an even number",
            "difficulty": "Easy",
            "question": "Is 14 even or odd? Enter even or odd.",
            "answer": "even",
            "hint": "An even number is divisible by 2.",
            "explanation": "14 % 2 = 0, so 14 is even."
        }
    ]
}

# Get saved progress from SQLite
saved_questions = database.get_solved_questions()
solved_ids = [row[0] for row in saved_questions]

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":
    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #4338ca, #db2777);
            padding: 28px;
            border-radius: 18px;
            color: white;
            margin-bottom: 24px;
        ">
            <h1 style="color: white; margin-bottom: 8px;">
                Welcome to AI Career Agent 🚀
            </h1>
            <p style="font-size: 16px; margin-bottom: 0;">
                Your personal companion for DSA practice,
                placement preparation, and career growth.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Welcome to your career dashboard!")

    st.subheader("Your Career Goal")
    st.info("Target: Software Development Engineer (SDE) Intern")

    total_count = sum(len(items) for items in questions.values())
    solved_count = len(solved_ids)

    col1, col2, col3 = st.columns(3)

    col1.metric("Questions Solved", solved_count)
    col2.metric("Accuracy", "Not tracked yet")
    col3.metric("Available Questions", total_count)

    progress = min(solved_count / total_count, 1) if total_count else 0

    st.subheader("Your Progress")
    st.progress(progress)
    st.write(f"{solved_count} of {total_count} questions completed.")

    st.subheader("Recently Completed Questions")

    if saved_questions:
        for question_id, title, topic, solved_at in saved_questions:
            st.write(f"✅ {title} — {topic}")
    else:
        st.info("No completed questions yet. Start practicing!")

    st.subheader("Your Next Step")
    st.write("Practice DSA problems and build your coding confidence.")

# =========================
# DSA PRACTICE
# =========================
    
    
    st.divider()
    st.subheader("📊 DSA Preparation Analytics")

    solved_questions = database.get_solved_questions()
    total_solved = len(solved_questions)
    dsa_goal = 100
    progress_percentage = min(total_solved / dsa_goal, 1.0)

    st.markdown("### 🎯 Overall DSA Goal")
    st.write(f"You have solved **{total_solved} / {dsa_goal} questions**")

    st.progress(progress_percentage)

    st.caption(
        f"{progress_percentage * 100:.1f}% completed "
        "toward your 100-question goal."
    )

    
    # Summary metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "✅ Questions Solved",
        total_solved
    )

    col2.metric(
        "📚 Topics Practiced",
        len(topic_counts) if "topic_counts" in locals() else 0
    )

    col3.metric(
        "🎯 Available Topics",
        3
    )


    topic_counts = {}

    for question in solved_questions:
        topic = question[2]
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
    
    if topic_counts:
        st.write("### Topic-wise Progress")

        for topic, count in topic_counts.items():
            st.write(f"**{topic}** — {count} question(s)")
            st.progress(count / total_solved)

        st.write("### 🥧 DSA Topic Distribution")

        chart_data = {
            "Topic": list(topic_counts.keys()),
            "Questions Solved": list(topic_counts.values()),
        }

        st.vega_lite_chart(
            chart_data,
            {
                "mark": {"type": "arc", "innerRadius": 50},
                "encoding": {
                    "theta": {
                        "field": "Questions Solved",
                        "type": "quantitative"
                    },
                    "color": {
                        "field": "Topic",
                        "type": "nominal"
                    },
                    "tooltip": [
                        {"field": "Topic", "type": "nominal"},
                        {
                            "field": "Questions Solved",
                            "type": "quantitative"
                        }
                    ]
                },
                "view": {"stroke": None}
            },
            use_container_width=True,
        )
    else:
        st.info(
            "No solved questions yet. Complete some questions "
            "in DSA Practice to see your analytics here!"
        )


elif page == "DSA Practice":

    st.header("💻 DSA Practice")
    st.write(
        "Choose a topic, solve a question, check your answer, "
        "and move to another challenge."
    )

    # 1. Select a topic
    topic = st.selectbox(
        "Choose a topic",
        list(questions.keys()),
        key="dsa_topic",
    )

    topic_questions = questions[topic]

    # 2. Keep track of the current question for each topic
    rotation_key = f"dsa_question_index_{topic}"

    if rotation_key not in st.session_state:
        st.session_state[rotation_key] = 0

    # Ensure the index remains valid
    current_index = st.session_state[rotation_key] % len(topic_questions)
    q = topic_questions[current_index]

    # 3. Display the current question
    st.subheader(q["title"])
    st.caption(f"Topic: {topic} | Difficulty: {q['difficulty']}")
    st.write(q["question"])

    with st.expander("💡 Show hint"):
        st.write(q["hint"])

    # 4. Answer input
    answer_key = f"dsa_answer_{topic}_{q['id']}"

    answer = st.text_input(
        "Your answer",
        key=answer_key,
        placeholder="Enter your answer here...",
    )

    # 5. Check answer
    if st.button("✅ Check Answer", key=f"check_{topic}_{q['id']}"):

        if not answer.strip():
            st.warning("Please enter your answer first.")

        elif answer.strip().lower() == str(q["answer"]).strip().lower():

            database.save_solved_question(
                q["id"],
                q["title"],
                topic,
            )

            st.session_state[f"dsa_completed_{q['id']}"] = True
            st.session_state[f"dsa_checked_{q['id']}"] = True

            st.success("🎉 Correct! Your progress has been saved.")

        else:
            st.session_state[f"dsa_checked_{q['id']}"] = True
            st.error("Not quite! Review the hint and try again.")

    # 6. Refresh saved progress
    saved_questions = database.get_solved_questions()
    solved_ids = [row[0] for row in saved_questions]

    if q["id"] in solved_ids:
        st.success("✅ Question completed!")

        with st.expander("📘 View explanation"):
            st.write(q["explanation"])

    # 7. Try another question at the bottom
    st.divider()

    if st.button(
        "🔄 Try Another Question",
        key=f"next_{topic}_{q['id']}",
        use_container_width=True,
    ):

        if len(topic_questions) > 1:
            # Move to the next question in this topic
            st.session_state[rotation_key] = (
                current_index + 1
            ) % len(topic_questions)

            # Clear the previous answer
            st.session_state.pop(answer_key, None)

            st.rerun()

        else:
            st.info(
                "There is only one question in this topic. "
                "Choose another topic or add more questions."
            )


# =========================
# AI RECOMMENDATIONS
# =========================
elif page == "AI Recommendations":

    st.header("🤖 AI Career Recommendations")

    st.write(
        "Get study suggestions based on your saved DSA progress."
    )

    saved_questions = database.get_solved_questions()
    solved_ids = [row[0] for row in saved_questions]
    solved_topics = [row[2] for row in saved_questions]

    st.subheader("Your Learning Analysis")
    st.metric("Questions Completed", len(solved_ids))

    all_topics = list(questions.keys())

    completed_by_topic = {
        topic: solved_topics.count(topic)
        for topic in all_topics
    }

    for topic in all_topics:
        st.write(
            f"**{topic}:** "
            f"{completed_by_topic[topic]} questions completed"
        )

    st.divider()
    st.subheader("🎯 Recommended Next Steps")

    next_question = None

    for topic in all_topics:
        for question in questions[topic]:
            if question["id"] not in solved_ids:
                next_question = question
                break
        if next_question:
            break

    if next_question:
        st.success(f"Recommended topic: {next_question['title']}")
        st.write(f"Topic: {next_question['title']}")
        st.write(next_question["hint"])
    else:
        st.success(
            "Excellent! You have completed all available questions. "
            "Add more questions to continue learning."
        )

    
    st.divider()
    st.subheader("✨ AI-Powered Career Advice")

    if st.button("Generate My AI Recommendations"):

        with st.spinner("Analyzing your progress..."):

            saved_questions = database.get_solved_questions()
            study_plan = database.get_study_plan()

            progress = "\n".join(
                f"- {row[1]} (Topic: {row[2]})"
                for row in saved_questions
            ) or "No questions completed yet."

            if study_plan:
                plan = (
                    f"Target date: {study_plan[0]}\n"
                    f"Daily hours: {study_plan[1]}\n"
                    f"Subjects: {study_plan[2].replace('|', ', ')}"
                )
            else:
                plan = "No study plan saved yet."

            prompt = f"""
You are an expert software engineering placement mentor.

Analyze this student's actual progress:
{progress}

Saved study plan:
{plan}

Provide:
1. Current preparation assessment.
2. Three prioritized next steps.
3. DSA topics to practice next.
4. A practical daily action plan.
5. One encouraging but realistic tip.

Do not invent completed work. Keep the advice beginner-friendly.
"""

            advice = ask_gemini(prompt)
            st.markdown(advice)


# =========================
# STUDY PLAN
# =========================


elif page == "AI Resume Analyzer":
    st.title("📄 AI Resume Analyzer")

    st.write(
        "Compare your resume with a job description "
        "and get personalized AI feedback."
    )

    st.divider()

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "txt"],
        key="resume_upload"
    )

    job_description = st.text_area(
        "Paste the job description here",
        placeholder="Paste the job requirements...",
        height=200,
        key="resume_job_description"
    )

    if st.button("Analyze My Resume", key="extract_resume"):
        if uploaded_resume is None:
            st.warning("Please upload your resume first.")

        elif not job_description.strip():
            st.warning("Please enter a job description.")

        else:
            try:
                resume_text = extract_resume_text(uploaded_resume)

                if resume_text.strip():
                    st.session_state["resume_text"] = resume_text
                    st.session_state["resume_job"] = job_description
                    st.session_state["resume_analysis"] = None

                    st.success("Resume text extracted successfully!")

                else:
                    st.warning(
                        "No readable text was found. "
                        "A scanned PDF may require OCR."
                    )

            except Exception as error:
                st.error(f"Could not read the resume: {error}")

    if st.session_state.get("resume_text"):
        with st.expander("Preview extracted resume text"):
            st.text(st.session_state["resume_text"][:4000])

        st.subheader("🤖 AI Resume Analysis")

        if st.button("Get AI Analysis", key="get_resume_analysis"):
            prompt = f"""
You are an expert technical recruiter.

Compare this resume with the job description.

RESUME:
{st.session_state["resume_text"][:12000]}

JOB DESCRIPTION:
{st.session_state["resume_job"][:8000]}

Give detailed feedback under these headings:

1. Resume suitability for the role
2. Relevant skills found in the resume
3. Missing or underrepresented skills
4. Project and experience improvements
5. ATS-friendly keyword suggestions
6. Three actionable recommendations

Be honest and specific. Do not invent qualifications,
experience, or skills that are not present in the resume.
"""

            with st.spinner("Gemini is analyzing your resume..."):
                analysis = ask_gemini(prompt)

            st.session_state["resume_analysis"] = analysis

        
    if st.session_state.get("resume_analysis"):
        st.markdown("### 📋 Your Resume Feedback")

        st.markdown(st.session_state["resume_analysis"])

        st.caption(
            "AI-generated feedback is an estimate, not an official ATS score."
        )






elif page == "AI Mock Interview":
    st.title("🎤 AI Mock Interview")

    st.write(
        "Practise placement interviews by speaking, typing answers, "
        "or writing code. Get personalized feedback from Gemini."
    )

    st.divider()

    # 1. INTERVIEW SETTINGS
    interview_type = st.selectbox(
        "Choose interview type",
        [
            "Technical Interview",
            "HR Interview",
            "Python Interview",
            "Project-Based Interview",
            "Coding Interview",
        ],
    )

    difficulty = st.selectbox(
        "Choose difficulty",
        ["Beginner", "Intermediate", "Advanced"],
    )

    role = st.text_input(
        "Target role",
        placeholder="e.g. Software Development Engineer Intern",
    )

    # 2. GENERATE QUESTION
    if st.button("🎯 Generate Interview Question"):
        if not role.strip():
            st.warning("Please enter your target role.")
        else:
            prompt = f"""
You are an experienced placement interviewer.

Generate ONE realistic interview question for the role: {role}.
Interview type: {interview_type}
Difficulty: {difficulty}

For a Coding Interview:
- Give a clear programming problem.
- Include an example input and expected output.
- Do not reveal the solution.

For other interview types:
- Ask one realistic, relevant interview question.
- Do not reveal the answer.

Return only the question and any necessary problem details.
"""

            with st.spinner("Preparing your interview question..."):
                question = ask_gemini(prompt)

            st.session_state["mock_interview_question"] = question
            st.session_state["mock_interview_type"] = interview_type
            st.session_state["mock_interview_role"] = role
            st.session_state["mock_interview_difficulty"] = difficulty

            for key in [
                "mock_interview_feedback",
                "mock_interview_transcript",
                "edited_mock_answer",
                "typed_mock_answer",
            ]:
                st.session_state.pop(key, None)

    question = st.session_state.get("mock_interview_question")

    if question:
        # 3. DISPLAY QUESTION
        st.subheader("🗣️ Your Interview Question")
        st.info(question)

        # 4. READ QUESTION ALOUD
        question_json = json.dumps(question)

        components.html(
            f"""
            <button onclick="speakQuestion()"
                style="
                    background: linear-gradient(90deg, #7c3aed, #db2777);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 12px 18px;
                    cursor: pointer;
                    font-size: 15px;
                ">
                🔊 Read Question Aloud
            </button>

            <script>
                const interviewQuestion = {question_json};

                function speakQuestion() {{
                    if (!("speechSynthesis" in window)) {{
                        alert("Speech playback is not supported.");
                        return;
                    }}

                    window.speechSynthesis.cancel();

                    const utterance = new SpeechSynthesisUtterance(
                        interviewQuestion
                    );

                    utterance.lang = "en-IN";
                    utterance.rate = 0.9;

                    window.speechSynthesis.speak(utterance);
                }}
            </script>
            """,
            height=55,
        )

        st.divider()

        # 5. LET THE USER CHOOSE HOW TO ANSWER
        st.subheader("✍️ Choose Your Answer Method")

        answer_mode = st.radio(
            "How would you like to answer?",
            [
                "🎙️ Speak My Answer",
                "⌨️ Type My Answer / Write Code",
            ],
            horizontal=False,
            key="mock_answer_mode",
        )

        submitted_answer = ""

        # OPTION A: SPEAK THE ANSWER
        if answer_mode == "🎙️ Speak My Answer":
            st.write(
                "Start speaking, then stop the recording. "
                "Your recognized answer will appear below."
            )

            attempt = st.session_state.get("mock_interview_attempt", 0)

            spoken_text = speech_to_text(
                language="en-IN",
                start_prompt="🎙️ Start Speaking",
                stop_prompt="⏹️ Stop Speaking",
                just_once=True,
                key=f"mock_interview_speech_{attempt}",
            )

            if spoken_text:
                st.session_state["mock_interview_transcript"] = spoken_text
                st.session_state.pop("mock_interview_feedback", None)
                st.session_state.pop("edited_mock_answer", None)

            transcript = st.session_state.get(
                "mock_interview_transcript", ""
            )

            if transcript:
                st.success("Speech converted into text!")

                submitted_answer = st.text_area(
                    "Review or correct your transcribed answer",
                    value=transcript,
                    height=180,
                    key="edited_mock_answer",
                )
            else:
                st.info(
                    "Your answer will appear here after speech "
                    "recognition returns a transcript."
                )

        # OPTION B: TYPE AN EXPLANATION OR WRITE CODE
        else:
            st.write(
                "Type your explanation or write your program below. "
                "For coding questions, include your code and reasoning."
            )

            submitted_answer = st.text_area(
                "Your answer / Python code",
                height=250,
                placeholder=(
                    "Example for a coding question:\n\n"
                    "def first_non_repeating(s):\n"
                    "    # Write your approach here\n"
                    "    pass\n\n"
                    "Explain your approach if needed."
                ),
                key="typed_mock_answer",
            )

        # 6. EVALUATE THE ANSWER
        if st.button("🤖 Evaluate My Answer"):
            if not submitted_answer.strip():
                st.warning(
                    "Please speak or type your answer before evaluation."
                )
            else:
                evaluation_prompt = f"""
You are an experienced placement interviewer and coding evaluator.

Candidate's target role:
{st.session_state.get("mock_interview_role", "")}

Interview type:
{st.session_state.get("mock_interview_type", "")}

Difficulty:
{st.session_state.get("mock_interview_difficulty", "")}

Interview question:
{question}

Candidate's answer:
{submitted_answer}

Evaluate the answer fairly and constructively.

For conceptual or HR questions, evaluate:
- Relevance and correctness
- Understanding and completeness
- Communication and clarity
- Practical examples where useful

For coding questions, evaluate:
- Whether the solution solves the stated problem
- Algorithm and logical reasoning
- Syntax and potential runtime errors
- Edge cases
- Time and space complexity, where applicable
- Possible improvements

If the candidate submits code, explain any bugs and show a corrected
solution when necessary. Do not claim code was executed or tested
unless it actually was.

Use these headings:

1. What Was Correct
2. What Was Missing or Incorrect
3. Technical Accuracy / Code Review
4. Edge Cases and Complexity (when applicable)
5. How to Improve
6. Sample Strong Answer or Corrected Code
7. Overall Score Out of 10

Be beginner-friendly, specific, and constructive.
Award marks based on the actual answer, not its length.
"""

                with st.spinner("Gemini is evaluating your answer..."):
                    feedback = ask_gemini(evaluation_prompt)

                st.session_state["mock_interview_feedback"] = feedback

        # 7. DISPLAY FEEDBACK
        feedback = st.session_state.get("mock_interview_feedback")

        if feedback:
            st.divider()
            st.subheader("📊 Your Interview Feedback")
            st.markdown(feedback)

            st.caption(
                "Review the feedback before moving to your next question."
            )

            # 8. TRY ANOTHER QUESTION — AT THE VERY END
            st.divider()

            if st.button(
                "🔄 Try Another Question",
                use_container_width=True,
            ):
                keys_to_clear = [
                    "mock_interview_question",
                    "mock_interview_type",
                    "mock_interview_role",
                    "mock_interview_difficulty",
                    "mock_interview_transcript",
                    "mock_interview_feedback",
                    "edited_mock_answer",
                    "typed_mock_answer",
                    "mock_answer_mode",
                ]

                for key in keys_to_clear:
                    st.session_state.pop(key, None)

                st.session_state["mock_interview_attempt"] = (
                    st.session_state.get("mock_interview_attempt", 0) + 1
                )

                st.rerun()



elif page == "Study Plan":

    from datetime import date

    st.header("📅 Your Personalized Study Plan")
    st.write(
        "Create a placement preparation schedule based on "
        "your target date, available hours, and learning goals."
    )

    # Load the previously saved plan
    existing_plan = database.get_study_plan()

    if existing_plan:
        default_date = date.fromisoformat(existing_plan[0])
        default_hours = float(existing_plan[1])
        default_topics = existing_plan[2].split("|")
    else:
        default_date = date.today()
        default_hours = 2.0
        default_topics = ["DSA", "Python"]

    st.subheader("⚙️ Customize Your Plan")

    with st.form("study_plan_form"):

        target_date = st.date_input(
            "Your placement preparation target date",
            value=max(default_date, date.today()),
            min_value=date.today()
        )

        daily_hours = st.slider(
            "How many hours can you study daily?",
            min_value=1,
            max_value=10,
            value=int(default_hours),
            step=1
        )

        topics = st.multiselect(
            "Choose the subjects you want to prepare",
            [
                "DSA",
                "Python",
                "SQL / DBMS",
                "Aptitude",
                "Core CS",
                "Technical Interviews",
                "HR Interviews"
            ],
            default=default_topics
        )

        submitted = st.form_submit_button("Generate My Study Plan")

    if submitted:

        if not topics:
            st.error("Please select at least one subject.")

        elif target_date < date.today():
            st.error("Please choose today or a future target date.")

        else:
            database.save_study_plan(
                target_date.isoformat(),
                daily_hours,
                topics
            )

            st.success("Your study plan has been saved!")

            st.rerun()

    # Display the saved plan
    saved_plan = database.get_study_plan()

    if saved_plan:

        saved_date = date.fromisoformat(saved_plan[0])
        hours = float(saved_plan[1])
        saved_topics = saved_plan[2].split("|")

        days_left = max((saved_date - date.today()).days, 0)

        st.divider()
        st.subheader("🎯 Your Preparation Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("Daily Study Hours", f"{hours:g} hrs")
        col2.metric("Days Until Target", days_left)
        col3.metric("Subjects Selected", len(saved_topics))

        st.progress(1 / len(saved_topics) if saved_topics else 0)

        st.subheader("📚 Your Daily Schedule")

        # Allocate study time across selected subjects
        minutes_available = int(hours * 60)
        base_minutes = minutes_available // len(saved_topics)
        extra_minutes = minutes_available % len(saved_topics)

        tasks = []

        for index, subject in enumerate(saved_topics):
            minutes = base_minutes + (
                1 if index < extra_minutes else 0
            )

            if subject == "DSA":
                task = "Solve coding problems and revise algorithms."
            elif subject == "Python":
                task = "Practice Python concepts and write code."
            elif subject == "SQL / DBMS":
                task = "Practice SQL queries and revise database concepts."
            elif subject == "Aptitude":
                task = "Solve quantitative and logical reasoning questions."
            elif subject == "Core CS":
                task = "Revise operating systems, networks, and OOP."
            elif subject == "Technical Interviews":
                task = "Practice technical questions and explain your projects."
            else:
                task = "Practice speaking clearly and answering HR questions."

            tasks.append({
                "subject": subject,
                "minutes": minutes,
                "task": task
            })

        for index, item in enumerate(tasks):
            with st.container(border=True):
                st.write(f"**{index + 1}. {item['subject']}**")
                st.write(f"⏱️ {item['minutes']} minutes")
                st.write(item["task"])

        st.caption(
            "This is a rule-based schedule. Later, we'll use AI "
            "to adapt your plan to your progress and weak areas."
        )

    else:
        st.info(
            "Choose your target date, daily hours, and subjects, "
            "then select Generate My Study Plan."
        )

# =========================
# AI CAREER CHAT
# =========================

# =========================
# AI CAREER CHAT
# =========================
elif page == "AI Career Chat":

    st.header("🤖 AI Career Chat")
    st.write(
        "Ask questions about DSA, Python, placements, "
        "technical interviews, or your career roadmap."
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask your career question..."):

        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                saved_questions = database.get_solved_questions()
                study_plan = database.get_study_plan()

                solved_list = [
                    f"- {row[1]} (Topic: {row[2]})"
                    for row in saved_questions
                ]

                progress_text = (
                    "\n".join(solved_list)
                    if solved_list
                    else "No DSA questions completed yet."
                )

                if study_plan:
                    plan_text = (
                        f"Target date: {study_plan[0]}\n"
                        f"Daily study hours: {study_plan[1]}\n"
                        f"Selected subjects: "
                        f"{study_plan[2].replace('|', ', ')}"
                    )
                else:
                    plan_text = (
                        "The student has not created a study plan yet."
                    )

                context = f"""
You are AI Career Agent, a personal placement preparation mentor.

Help a computer science student prepare for SDE internships and jobs.
Explain concepts in beginner-friendly language with examples.

STUDENT'S SAVED PROGRESS:
{progress_text}

STUDENT'S STUDY PLAN:
{plan_text}

Use the saved information when relevant. Do not invent progress.
Give practical, clear, encouraging advice.

STUDENT'S QUESTION:
{prompt}
"""

                reply = ask_gemini(context)
                st.markdown(reply)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
