import streamlit as st
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)

def generate_grammar_excercise():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a language teacher. your job is to tech people english grammar, via fun and interesting short exercises by sharing with them some fill in the blanks or multiple choice questions. Please give one question only"
            },
            {
                "role": "user",
                "content": "Create a fun grammar exercise (fill in the blanks or multiple choice) based on English language. Please give one question only"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()

def check_answer(question, user_answer):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role":"system",
                "content": "You are a language teacher. your job is to tech people english grammar. you will be give a question and an answer, both by the user. you have to evaluate it and share feedback. please be supportive and helpful."
            },
            {
                "role":"user",
                "content": f"Question: {question}\nAnswer: {user_answer}\n Evaluate the correctness of the answer and provide feedback"
            }
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()

def app():
    st.header("Grammar and Fun")
    st.write("Sharpen your grammar skills with these excercises.")

    if 'excercise' not in st.session_state:
        st.session_state.excercise = None
    if 'user_response' not in st.session_state:
        st.session_state.user_response = ''

    if st.button('Start'):
        st.session_state.excercise = generate_grammar_excercise()
    
    if st.session_state.excercise:
        st.subheader('Excercise')
        st.write(st.session_stat.excercise)

        user_response = st.text_input("Your answer", key="response")

        if st.button('Check Answer'):
            if user_response:
                st.session_state.user_response = user_response
                feedback = check_answer(st.session_state.excercise, user_response)
                st.subheader('Feedback:')
                st.write(feedback)
            else:
                st.error("Please enter an answer before checking")