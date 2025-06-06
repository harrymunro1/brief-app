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



st.write("# Introduction")

