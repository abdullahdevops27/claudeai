import streamlit as st
import os
from PyPDF2 import PdfReader
from pydantic import validator
from anthropic import Anthropic

st.set_page_config("Research PDF Summarizer", page_icon=":memo:")

st.title("Research PDF Insights Extractor")

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

uploaded_file=st.file_uploader("Select a PDF", type="pdf")

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)

    text = ""
    for page in pdf_reader.pages:
        text +=page.extract_text()

    st.subheader("Extracted PDF Contents")
    st.text_area("",value=text,height=300)

    with open("./system_prompt.txt" , "r") as f:
        system_prompt=f.read()

    main_prompt = "Here is an academic paper: <paper>{}</paper>"

    if st.button('Extract Insights'):
        response = client.messages.create(
            system = system_prompt,
            max_tokens =1024,
            model = "claude-3-haiku-20240307",
            temperature =0.5,
            messages =[ 
                {"role":"user","content":main_prompt.format(text)}
            ]
            )
        
        st.subheader("Extracted Insights")
        if response.content:
            st.write(response.content[0].text)
