import streamlit as st
# from dotenv import load_dotenv
import base64
# import os




# Load environment variables from .env file
# load_dotenv()

# Load .png file
# Encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("kantarworldpanel_logo.png")


# Inject custom CSS to place the image
st.markdown(f"""
    <style>
    .top-right-logo {{
        position: fixed;
        top: 30px;
        right: 125px;
        width: 300px;
        z-index: 100;
    }}
    </style>
    <img class="top-right-logo" src="data:image/png;base64,{img_base64}">
""", unsafe_allow_html=True)



# # Get password from .env
# correct_password = os.getenv("APP_PASSWORD")

# # Simple password protection
# def check_password():
#     entered_password = st.text_input("Enter password:", type="password")
#     if entered_password == correct_password:
#         st.session_state["authenticated"] = True
#     elif entered_password:
#         st.error("Incorrect password")

# # Check if user is authenticated
# if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
#     check_password()
#     st.stop()


# -- Page setup -- 
about_page = st.Page(
    page = "views/about.py",
    title = "Introduction",
    icon = ":material/account_circle:",
    default=True
    )

brief_page = st.Page(
    page = "views/brief-app2.py",
    title = "Brief Helper",
    icon = ":material/account_circle:"
    )

email_page = st.Page(
    page = "views/email.py",
    title = "Email Helper",
    icon = ":material/mail:"
    )


# -- Navigation --
# pg = st.navigation(pages=[brief_page,email_page])
pg = st.navigation(
    {
     "Info": [about_page],
     "Apps":[brief_page,email_page]
    }
 )
st.sidebar.text("Made by Harry Munro ✨")

pg.run()









