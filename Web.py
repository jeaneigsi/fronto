import os
import streamlit as st
from streamlit_javascript import st_javascript
from PIL import Image
import re
from io import BytesIO

import screenshot_to_code
import trulens  


    


if "has_download" not in st.session_state:
    st.session_state.has_download = False

if "improved" not in st.session_state:
    st.session_state.improved = False

st.set_page_config(layout="wide")

# Change the title
#st.title("""Fronto 🧑‍💻""")

    # Centered title
st.markdown("""
    <div style="text-align:center">
        <h1>Fronto 🧑‍💻</h1>
        <h2>(Build your website in 1 Min)</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a horizontal line for separation
st.markdown("---")
    
    # Subtitle
st.markdown("## ScreenShot to code 🌅 & Image Link to code 📱")
    
    # Add a horizontal line for separation
st.markdown("---")
    
    # Subtitle
st.markdown("## Then evalute the perfomance by Trulens 🦑")



# Create a navigation bar
nav_option = st.sidebar.radio("Navigation", ("Image Link 📱", "Upload ScreenShot 🌅"))

def main():
    # Javascript variables
    window_width = st_javascript("window.innerWidth")
    hostname = st_javascript("window.location.hostname")

    # Set Clarify PAT from secrets
    clarifai_pat = st.secrets["CLARIFAI_PAT"]

    option = None

    if nav_option == "Image Link 📱":
        option = "Image URL"
        IMAGE_URL = st.text_input(
            "Enter the image URL to get started!",
            "https://cdn-images-1.medium.com/v2/resize:fit:1200/1*y0EOSRFSeRQzMb100X6Sog.png",
        )
        if IMAGE_URL is not None:
            st.image(BytesIO(screenshot_to_code.get_image_from_url(IMAGE_URL)), width=700)

    elif nav_option == "Upload ScreenShot 🌅":
        option = "Upload Image"
        IMAGE_FILE = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if IMAGE_FILE is not None:
            st.image(IMAGE_FILE, width=700)

    if option:
        llm = st.radio("LLM:", ("GPT-4",))

        if st.button("Build Website 🧑‍💻"):
            if not clarifai_pat:
                st.warning("Please enter your PAT to continue:", icon="⚠️")
            else:
                os.environ["CLARIFAI_PAT"] = clarifai_pat

                if option == "Image URL":
                    screenshot_to_code.buildWebsite(IMAGE_URL, option="Image URL", llm=llm)
                    st.session_state.has_download = True

                elif option == "Upload Image":
                    if IMAGE_FILE is not None:
                        screenshot_to_code.buildWebsite(
                            IMAGE_FILE, option="Upload Image", llm=llm
                        )
                        st.session_state.has_download = True
                    else:
                        st.warning("Please upload an image to continue:", icon="⚠️")

    file_path_html = "./my_website/index.html"
    file_path_css = "./my_website/styles.css"

    if os.path.exists(file_path_html) and os.path.exists(file_path_css):
        with open(file_path_html, "r", encoding="utf8") as file:
            html_string = file.read()
        with open(file_path_css, "r", encoding="utf8") as file:
            css_string = "<style>" + file.read() + "</style>"

        html_plus_css = re.sub(r"<link.*?css.*?>", css_string, html_string)

        st.components.v1.html(
            html_plus_css,
            width=window_width,
            height=window_width / 16 * 9,
        )

    st.subheader("Click to download the code ✅")
    st.download_button(
        label="Download Code",
        data=open("my_website.zip", "rb").read(),
        key="download_directory",
        file_name="my_website.zip",
    )

if __name__ == "__main__":
    main()
