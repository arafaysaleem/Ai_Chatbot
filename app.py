import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI

# OpenAI API Key (Set your own API Key)
client = OpenAI(api_key="")

# Function to generate AI response
def chat_with_ai(user_input):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": user_input}])
    return response.choices[0].message.content

# Function to convert text to speech
def text_to_speech(response_text):
    tts = gTTS(text=response_text, lang="en")
    audio_file = "response.mp3"
    tts.save(audio_file)
    return audio_file

# Function to recognize speech from microphone
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_text = recognizer.recognize_google(audio)
            return user_text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "API Error. Please try again."

# Initialize session state for user_query
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

# Streamlit UI
st.title("🎙️ AI Chatbot with Voice")
st.write("Chat with AI using text or voice!")

# Voice Input
if st.button("🎤 Speak"):
    st.session_state.user_query = speech_to_text()
    st.text(f"**You said:** {st.session_state.user_query}")
else:
    st.session_state.user_query = st.text_input("Type your message:", st.session_state.user_query)

# Process User Query
if st.button("Send") and st.session_state.user_query:
    ai_response = chat_with_ai(st.session_state.user_query)
    st.session_state.user_query = ""

    # Display AI Response
    st.success(f"🤖 AI: {ai_response}")

    # Convert Response to Speech
    audio_path = text_to_speech(ai_response)
    st.audio(audio_path, format="audio/mp3")
