# ShotGame

**ShotGame** is a web-based calculus quiz platform built with **Django**. The application generates random calculus questions using **Groq AI**, tracks user scores per session, and provides an interactive quiz experience.  

---

## Features

- **Dynamic Question Generation**  
  Uses Groq AI to generate calculus questions with 4 multiple-choice options.

- **REST API Endpoints**  
  Provides endpoints for fetching questions and submitting answers:
  - `GET /api/get_question` → Returns a random calculus question with options.
  - `POST /api/check_answer` → Validates a submitted answer.

- **Front-End Integration**  
  Simple HTML templates render questions, options, and results.

- **Extensible & Modular**  
  Easily extendable for additional topics, question types, or scoring mechanisms.

---

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework  
- **AI Integration:** Groq (Llama 3.1 model)  
- **Database:** SQLite/MySQL/TiDB Cloud  
- **Frontend:** HTML/CSS, Django Templates  
- **Environment Management:** python-dotenv  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/shotgame.git
cd shotgame
```

2. **Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
3. **Create a .env file in the project root:**
```bash
GROQ_API_KEY=your_groq_api_key_here
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

---

## Usage
Navigate to the home page to get a random question.
Select an option and submit your answer.
