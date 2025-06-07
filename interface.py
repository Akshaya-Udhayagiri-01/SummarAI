import streamlit as st
from text import summarize_text
import PyPDF2
import io

st.set_page_config(page_title="SummarAI", page_icon="🧠", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>🧠 SummarAI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Paste or upload a long article and get a smart summary instantly</h4>", unsafe_allow_html=True)
st.markdown("---")

# Input options
input_mode = st.radio("Choose input method:", ("📝 Paste Text", "📁 Upload File"))

text_input = ""

# Option 1: Paste text
if input_mode == "📝 Paste Text":
    text_input = st.text_area("Paste your paragraph or article:", height=250, placeholder="Enter long text here...")
    if text_input:
        st.caption(f"📝 Word count: {len(text_input.split())}")

# Option 2: Upload file
else:
    uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            text_input = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_input = ""
            for page in pdf_reader.pages:
                text_input += page.extract_text() or ""
        st.text_area("Extracted Text (Editable):", value=text_input, height=250)

# ---- Summarize Button ----
summarize_clicked = st.button("✨ Summarize", key="summarize_button")

if summarize_clicked:
    if text_input.strip():
        with st.spinner("Summarizing..."):
            summary = summarize_text(text_input)
        st.markdown("### ✅ Summary:")
        st.success(summary)
    else:
        st.warning("Please provide some text.")

# ---- Footer ----
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made with ❤️ using BART by Hugging Face</div>", unsafe_allow_html=True)
