# 🤖 AI Career Agent

An AI-powered career preparation platform built with Python and Streamlit to help students prepare for technical interviews, improve their DSA skills, analyze resumes, and plan their placement preparation.

## ✨ Features

- **Dashboard:** Track solved DSA questions and monitor preparation progress.
- **DSA Practice:** Practice coding concepts, check answers, and view hints and explanations.
- **AI Recommendations:** Get personalized career preparation recommendations using Google Gemini.
- **Study Planner:** Create a study plan based on your target date and available daily study hours.
- **AI Career Chat:** Ask career-related questions and get AI-powered guidance.
- **AI Resume Analyzer:** Upload a PDF or TXT resume and receive feedback based on a target job description.
- **AI Mock Interview:** Practice interview questions, submit spoken or typed answers, and receive AI-generated feedback.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- SQLite
- Pandas
- PyPDF
- Python dotenv

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-career-agent.git
cd ai-career-agent
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key. **Never upload your `.env` file or expose your API key on GitHub.**

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal to use the application.

## 📁 Project Structure

```text
ai-career-agent/
├── app.py
├── database.py
├── ai_helper.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

The SQLite database is created locally when the application runs.

## 🎯 Project Objective

The goal of AI Career Agent is to bring career guidance, coding practice, personalized study planning, resume feedback, and mock interview practice into one accessible platform for students preparing for internships and placement opportunities.

## 🔮 Future Enhancements

- Expand the DSA question bank.
- Add more detailed progress analytics.
- Improve personalized learning recommendations.
- Add more interview categories and difficulty levels.
- Deploy the application online for public access.

## 👩‍💻 Author

**Pravallika Madiraju**

- GitHub: [pravallikam357-ai](https://github.com/pravallikam357-ai)
- LinkedIn: [Pravallika Madiraju](https://www.linkedin.com/in/pravallika-madiraju/)
