# Similar Question Finder

## Option Chosen

Option B: Similar Question Finder with Auto-Tagging

---

## Overview

Similar Question Finder is an AI-powered web application that allows students to ask study questions and find semantically similar previous questions. The system automatically detects the topic of the question and stores the search history.

---

## Features

- User Signup and Login
- Automatic Topic Detection
- Similar Question Search
- Question History
- Topic Filtering
- SQLite Database Storage
- Semantic Similarity Matching
- React Frontend
- Flask Backend

---

## Tech Stack

### Frontend
- React
- Bootstrap
- Vite

### Backend
- Flask
- Flask SQLAlchemy
- Flask CORS

### Database
- SQLite

### AI / ML
- Sentence Transformers
- Cosine Similarity
- Scikit-learn

---

## How It Works

### Topic Detection

The backend automatically assigns a topic to a question using keyword-based classification.

Examples:

- Photosynthesis → Biology
- Force → Physics
- Algebra → Math

### Similarity Search

1. User enters a question.
2. Sentence Transformer converts the question into an embedding vector.
3. Existing questions are converted into vectors.
4. Cosine Similarity is calculated.
5. Most similar questions are returned.

---

## Project Structure

```
SimilarQuestionFinder
│
├── backend
│   ├── app.py
│   └── database.db
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
└── README.md
```

---

## Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## API Endpoints

### Signup

POST

```
/signup
```

### Login

POST

```
/login
```

### Add Question

POST

```
/add-question
```

### Similar Questions

POST

```
/similar
```

### History

GET

```
/history/<user_id>
```

---

## Author

Kani

BE Electronics and Communication Engineering