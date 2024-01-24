import os
import sqlite3
import streamlit as st
import dotenv 

dotenv.load_dotenv()

import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


def gemini_get(prompt, question):
    """
    Generates content using the gemini-pro GenerativeModel with the given prompt and question.

    Args:
        prompt (list): The prompt for content generation.
        question (str): The question to be used with the prompt.

    Returns:
        str: The generated content.
    """
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    
    return response.text

def read_sql(sql,db):
    """
    Reads data from the specified SQL database using the provided SQL query.

    Args:
        sql (str): The SQL query to be executed.
        db (str): The path to the SQLite database.

    Returns:
        list: A list of tuples, each representing a row of the query result.
    """
    
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    
    for i in rows:
        print(i)
        
    return rows
    


prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """
]

def ask_question():
    """
    Launches a Streamlit web interface for an English to SQL chatbot. Users input English questions, 
    and the chatbot generates corresponding SQL queries using the Gemini model. 
    The generated SQL queries are executed on a SQLite database, and results are displayed.
    
    Takes no parameters and has no return type.
    """
    
    st.set_page_config(page_title="eng->sql")
    st.header("english -> sql ")

    question = st.text_input("Input: ", key="input")
    submit = st.button("ask the question")

    if submit:
        sql_query = gemini_get(prompt, question)
        st.subheader("SQL Query:")
        st.code(sql_query)

        response = read_sql(sql_query, "student.db")
        st.subheader("Answer:")
        
        for i in response:
            st.write(i)


if __name__ == "__main__":
    ask_question()