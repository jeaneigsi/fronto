import streamlit as st
import os
from pathlib import Path

import google.generativeai as genai
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from clarifai.client.model import Model
from clarifai.client.input import Inputs

import screenshot_to_code



inference_params = dict(temperature=0.2, max_tokens=250)
conversation = ""

info_prompt = """What is inside of this image? You need to give me information 
                about colors, padding and layout, data inside table/elements, text in the image"""

info_prompt_0 = """What is inside of this image? You need to give me information 
                             about colors, padding, navigation bar/hamburger menu, data inside table, text in the image"""

info_prompt_1 = """What is inside of this image? You need to give me information 
                             about colors, padding, navigation bar/hamburger menu, data inside table, text/textsize in the image"""

def getGPT4VisionResponse(image, prompt, option):

    used_info_prompt = info_prompt_1
    if option == "Image URL":
        r1 = chatbotImageURL(
            image_url=image,
            input=used_info_prompt,
        )
        print("r1: " + r1)
        r2 = chatbotImageURL(image_url=image, input=prompt)

    elif option == "Upload Image":
        r1 = chatbotImageFile(image_file=image, input=used_info_prompt)
        print("r1: " + r1)
        r2 = chatbotImageFile(image_file=image, input=prompt)



def getGPT4Response(prompt):
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/GPT-4"
    ).predict_by_bytes(
        prompt.encode(), input_type="text", inference_params=inference_params
    )

    response = model_prediction.outputs[0].data.text.raw
    return response


def chatbotImageFromFilePath(input, file_path):
    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()

    global conversation
    conversation += "user: " + input + "\n\n"
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    ).predict(
        inputs=[
            Inputs.get_multimodal_input(
                input_id="", image_bytes=image_bytes, raw_text=conversation
            )
        ],
        inference_params=inference_params,
    )
    response = model_prediction.outputs[0].data.text.raw
    conversation += "assistant: " + response + "\n\n"
    return response


def chatbotImageFile(input, image_file):
    # Temporarily saves the file to directory and read in as bytes
    uploaded_file = image_file
    file_path = os.path.join("tmpDirUploadedImage", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with open('./image_feedback/input_mock_website.png', "wb") as f:
        f.write(uploaded_file.getbuffer())


    return chatbotImageFromFilePath(input, file_path)


def chatbotImageURL(input, image_url):
    image_bytes = screenshot_to_code.get_image_from_url(image_url)
    with open('./image_feedback/input_mock_website.png', "wb") as f:
        f.write(image_bytes)

    global conversation
    conversation += "user: " + input + "\n\n"
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    ).predict(
        inputs=[
            Inputs.get_multimodal_input(
                input_id="", image_url=image_url, raw_text=conversation
            )
        ],
        inference_params=inference_params,
    )
    response = model_prediction.outputs[0].data.text.raw
    conversation += "assistant: " + response + "\n\n"
    return response

