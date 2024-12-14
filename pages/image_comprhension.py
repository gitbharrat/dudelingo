import streamlit as st
import requests
import numpy as np
import sounddevice as sd
import io
import wave
from openai import OpenAI
from scipy.io.wavfile import write
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def speech_to_text(file_path):
    audio_file = open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    print("Transcript:")
    print(transcription.text)
    return transcription.text


def describe_image(image_url):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image like an IELTS exam."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    print("Description:")
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def compare_descriptions(model_desc, user_desc):
    st.write(f"Description: {model_desc}")
    st.write(f"User Description: {user_desc}")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a language teacher. you have a predefined description of an image, and also a user written dscription. you just have to judge the language, grammer and vocabolary of the user provided description. keep in mind that the user is a beginner so be supportive and helpful.",
            },
            {
                "role": "user",
                "content": f"Description: {model_desc},user Description: {user_desc}. based on these two respond what all the user can improve in their description of the image ",
            },
        ],
    )
    print("completion.choices[0].message.content")
    st.subheader("Feedback")
    st.write(f"Analysis: {completion.choices[0].message.content.strip()}")


def app():
    st.header("Image Comprehension")
    st.write(
        "Learn to understand and describe image in your target language. Thhis task focuses on improving your speaking skills and vocabulary."
    )

    if "image_shown" not in st.session_state:
        st.session_state.image_shown = False
    if "recording_started" not in st.session_state:
        st.session_state.recording_started = False

    if st.button("Start"):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        print(st.session_state.image_generated)
        if st.session_state.image_generated == False:
            url = f"https://picsum.photos/1280/720"
            response = requests.get(url)
            image_url = response.url
            st.session_state.image_url = image_url
            st.session_state.image_generated = True
            print(st.session_state.image_generated)

        st.image(st.session_state.image_url, caption="Describe this image.")
        st.subheader(
            "You have to describe and talk about what you see in the image. Take yur time look and analyse the image think about what you want to say and then start.\n You will have 30 seconds to speak about it. Focus on rich decription fluid speech."
        )

        if st.button("Start Talking"):
            st.session_state.recording_started = True
            duration = 5
            sample_rate = 44100

            st.write("Recording started....")
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
            )
            sd.wait()
            st.write("Recording Stopped!")

            st.session_state.recording_started = False
            output_file = "output2.wav"

            with wave.open(output_file, "w") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(recording.tobytes())

            print(f"Audio saved to {output_file}")
            user_description = speech_to_text(output_file)
            model_description = describe_image(st.session_state.image_url)
            compare_descriptions(model_description, user_description)
