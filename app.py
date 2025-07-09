import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for PDF
import google.generativeai as genai

# Streamlit page setup
st.set_page_config(page_title="Medical Diagnosis AI Assistant", layout="centered")

st.title("🧠 Medical Diagnosis Interpreter")
st.markdown("""
Upload a **CSV, Excel, or PDF file**, or **paste the test results** below. 
This AI tool will analyze the content and suggest possible diagnoses based on the information.
""")

# Configure Gemini API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("models/gemini-pro")  # ✅ Correct model path for v1

# File upload
uploaded_file = st.file_uploader("📂 Upload medical report (CSV, Excel, or PDF)", type=["csv", "xlsx", "xls", "pdf"])

# Text input
text_input = st.text_area("📝 Or paste clinical/lab results manually below:", height=200)

# Button to analyze
if st.button("🩺 Interpret Results"):
    combined_text = ""

    # Handle file input
    if uploaded_file:
        file_type = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_type == "csv":
                df = pd.read_csv(uploaded_file)
                combined_text += df.to_string(index=False)
            elif file_type in ["xlsx", "xls"]:
                df = pd.read_excel(uploaded_file)
                combined_text += df.to_string(index=False)
            elif file_type == "pdf":
                text = ""
                pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in pdf:
                    text += page.get_text()
                combined_text += text.strip()
        except Exception as e:
            st.error(f"❌ Failed to read uploaded file: {e}")

    # Add manual text
    if text_input.strip():
        combined_text += "\n\n" + text_input.strip()

    # Analyze combined content
    if combined_text.strip() == "":
        st.warning("Please provide some medical content to analyze.")
    else:
        with st.spinner("Analyzing patient data..."):
            prompt = f"Based on these medical test results or descriptions, what could be the possible diagnosis?\n\n{combined_text}\n\nExplain simply."
            try:
                response = model.generate_content([prompt])  # ✅ Gemini expects a list of strings
                st.success("✅ Possible Interpretation:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"❌ Gemini error: {e}")
