# English to SQL Chatbot

## Overview

This project combines a SQLite database with a Streamlit app to create a simple English to SQL chatbot. Users input English questions related to a predefined prompt, and the chatbot generates corresponding SQL queries. These queries are executed on a SQLite database, and the results are displayed using Streamlit.

## Setup

1. Create and activate a virtual environment:
    ```bash
    python -m venv venv

    source venv/bin/activate  # for Linux,MacOS systems
    venv\Scripts\activate # for Windows 
    ```

2. Install required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up a `.env` file with your Gemini API key.

4. Run the SQLite script to create the database and insert initial values:
    ```bash
    python sqlite.py
    ```

5. Run the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```

6. Open the provided Streamlit link in your web browser.

## Usage

1. Input an English question in the provided text input.

2. Click "Ask the Question" to generate the SQL query.

3. View the generated SQL query and the corresponding results from the SQLite database.