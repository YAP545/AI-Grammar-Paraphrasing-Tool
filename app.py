import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Grammar Tool", layout="centered")

st.title("✍️ AI Grammar & Paraphrasing Tool")
st.write("Improve your sentences instantly using AI")

# User input
user_input = st.text_area("Enter your sentence:")

# Options
tone = st.selectbox("Select Tone", ["Formal", "Informal"])
length = st.selectbox("Select Output Length", ["Short", "Detailed"])

def generate_output(text, tone, length):
    prompt = f"""
    Correct the grammar and rewrite the sentence.

    Tone: {tone}
    Length: {length}

    Sentence:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert English editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


if st.button("✨ Improve Sentence"):
    if user_input.strip() == "":
        st.warning("Please enter some text")
    else:
        with st.spinner("Processing..."):
            result = generate_output(user_input, tone, length)
            st.success("Done!")
            st.write("### ✨ Improved Sentence:")
            st.write(result)
