import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF

# Load Hugging Face models
summarizer = pipeline("summarization")
qa_model = pipeline("question-answering")

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question(question, context):
    answer = qa_model(question=question, context=context)
    return answer['answer']

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Custom CSS
st.markdown(
    """
    <style>
    .css-18e3th9 {
        background-color: #FFFFFF;
    }
    .css-1d391kg {
        background-color: #F0F2F6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Assistant")

menu = ["Summarize PDF", "Ask a Question"]
choice = st.sidebar.selectbox("Choose an action", menu)

if choice == "Summarize PDF":
    st.header("Summarize PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Text")
        st.write(text[:1000] + "...")  # Display first 1000 characters for readability
        summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)

elif choice == "Ask a Question":
    st.header("Ask a Question")
    context = st.text_area("Enter the context (e.g., a paragraph from a document)")
    question = st.text_input("Enter your question")
    if st.button("Get Answer"):
        if context and question:
            answer = answer_question(question, context)
            st.subheader("Answer")
            st.write(answer)
        else:
            st.error("Please provide both context and a question.")