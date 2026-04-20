import streamlit as st
from groq import Groq

# Load API key from Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY")

# Stop if API key missing
if not api_key:
    st.error("❌ API key not found. Add GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Page config
st.set_page_config(page_title="AI Grammar Tool", layout="centered")

# UI
st.title("✍️ AI Grammar & Paraphrasing Tool")
st.write("Improve your sentences instantly using AI")

# Input
user_input = st.text_area("Enter your sentence:")

# Options
tone = st.selectbox("Select Tone", ["Formal", "Informal"])
length = st.selectbox("Select Output Length", ["Short", "Detailed"])

# Function
def generate_output(text, tone, length):
    if not text or text.strip() == "":
        return "⚠️ Please enter a valid sentence."

    prompt = f"""
Correct the grammar and rewrite the sentence.

Tone: {tone}
Length: {length}

Sentence:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Updated working model
            messages=[
                {"role": "system", "content": "You are an expert English editor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Button
if st.button("✨ Improve Sentence"):
    if not user_input or user_input.strip() == "":
        st.warning("Please enter some text")
    else:
        with st.spinner("Processing..."):
            result = generate_output(user_input, tone, length)
            st.success("Done!")
            st.write("### ✨ Improved Sentence:")
            st.write(result)
