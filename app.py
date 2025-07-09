import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Medical Diagnosis AI Assistant", layout="centered")

st.title("🧠 Medical Diagnosis Interpreter")
st.markdown("Upload patient lab results and let AI help doctors interpret them.")

# API Key setup
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Create AI model
model = genai.GenerativeModel("models/gemini-pro")

# Input fields
results = st.text_area("🔬 Paste the lab test results or clinical notes here:", height=200)

if st.button("🩺 Interpret Results"):
    if results.strip():
        with st.spinner("Analyzing patient data..."):
            prompt = f"Based on these medical test results or descriptions, what could be the possible diagnosis?\n\n{results}\n\nExplain simply."
            response = model.generate_content([prompt])
            st.success("✅ Possible Interpretation:")
            st.markdown(response.text)
    else:
        st.warning("Please paste some patient results to proceed.")
