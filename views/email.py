from langchain.prompts import PromptTemplate
import streamlit as st
from docx import Document
import re
import urllib.parse
import os
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()



st.write("# Email Helper")
st.write("This app is designed to take in a brief recommendation and setup an email prompt to the correct people")



# Get api key
api_key = os.getenv("OPENAI_API_KEY")


# get the client name
client = st.text_input("Client name:")

## Input recommendation
doc = Document(st.file_uploader("Upload **brief recommendation**, often saved in your downloads folder:",
                                 type=["docx"]))
rec_text = "\n".join([para.text for para in doc.paragraphs])
emails = list(set(re.findall(r'\b[\w\.-]+@[Kk]antar\.com\b', rec_text)))

# Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

gen_emails = st.button("Generate prompt")

if gen_emails:
    
    ### Recipients 
    
    # st.write("These are the emails found in the recomendation:")
    # st.write(emails)
    
        # Join them into a single string
    to = ";".join(emails)
    
    
    
    
    ### Subject
    
    # Create prompt for the LLM
    prompt = PromptTemplate(
        input_variables=["rec_text"],
        template=
        """
        Can you return just the name of the project that is being advised in the recommendation.
        Make sure you only return the project name and NOTHING else.
        
        recommendation:
        {recommendation}
        """
    )
    # Get LLM recommendation
    llm = ChatOpenAI(
                temperature=0.3,
                model_name="gpt-3.5-turbo",
                # model_name="gpt-4",
                #model_name="gpt-4-turbo",
                max_tokens=200,
                 openai_api_key=api_key
            )
    
        # Create the chain
    chain = prompt | llm
    
    # Use `.invoke()` instead of `.run()`
    response_proj = chain.invoke({
        "recommendation": rec_text
    })
    
    
    ### Summary 
    # Create prompt for the LLM
    prompt = PromptTemplate(
        input_variables=["rec_text"],
        template=
        """
        Can you summarise this in no more than 60 words, mainly from the clients point of view 
        about WHY they need this project that is being recommended.Dont put mucg information about the project as this is being sent to an expert of the project.
        No need to mention about contact information as this is being shared to them anyway.
        
        recommendation:
        {recommendation}
        """
    )
    # Get LLM recommendation
    llm = ChatOpenAI(
                temperature=0.3,
                model_name="gpt-3.5-turbo",
                # model_name="gpt-4",
                #model_name="gpt-4-turbo",
                max_tokens=200,
                 openai_api_key=api_key
            )
    
        # Create the chain
    chain = prompt | llm
    
    # Use `.invoke()` instead of `.run()`
    response_sum = chain.invoke({
        "recommendation": rec_text
    })
    
    
    
    
    
    subject = response_proj.content + " Opportunity for "+ client
    body = "Hi everyone,\n\nI have recently had a client brief from "+client+", and have been recommended to look into our "+response_proj.content+" solution.\n\nHere is the reason for this recommendation:\n\""+response_sum.content+"\"\n\nIt would be good to get your thoughts on this!\n\nThanks."
    
    # Encode subject and body
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    
    # Build the mailto link
    url = f"mailto:{to}?subject={subject_encoded}&body={body_encoded}"
        
    # Create a clickable link in Streamlit
    st.markdown(f"[📧 Click here to open email prompt]({url})", unsafe_allow_html=True)
