# Similar Question Finder

## Overview

Similar Question Finder is an AI-powered web application that helps users find semantically similar questions using Sentence Transformers.

## Features

* React Frontend
* Flask Backend
* SQLite Database
* Topic Detection
* AI Similarity Search
* Duplicate Question Prevention

## Technologies Used

* React
* Flask
* SQLite
* Sentence Transformers
* Scikit-learn

## How to Run

### Backend

cd backend

venv\Scripts\activate

python app.py

### Frontend

cd frontend

npm install

npm run dev

## Project Flow

User enters a question

↓

Question is saved in SQLite database

↓

Sentence Transformer generates embeddings

↓

Cosine Similarity is calculated

↓

Similar questions are displayed with similarity percentage and topic
