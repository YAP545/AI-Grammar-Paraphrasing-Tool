import streamlit as st
from groq import Groq

# Load API key from Streamlit secrets
api_key = st.secrets.get("GROQ_API_KEY")

if not api_key:
    st.error("API key not found")
    st.stop()

client = Groq(api_key=api_key)

st.title("✍️ AI Grammar & Paraphrasing Tool")

user_input = st.text_area("Enter your sentence:")

tone = st.selectbox("Select Tone", ["Formal", "Informal"])
length = st.selectbox("Select Output Length", ["Short", "Detailed"])

def generate_output(text, tone, length):
    prompt = f"""
    Correct grammar and rewrite the sentence.

    Tone: {tone}
    Length: {length}

    Sentence:
    {text}
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert English editor."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if st.button("✨ Improve Sentence"):
    if not user_input.strip():
        st.warning("Please enter some text")
    else:
        with st.spinner("Processing..."):
            result = generate_output(user_input, tone, length)
            st.success("Done!")
            st.write(result)
