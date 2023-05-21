import streamlit as st
import requests
import json
import openai
import numpy as np
from azure.storage.blob import BlobServiceClient
import io

openai.api_key = ""

def get_lan(comment, lan="en"):
    # Using the api call to translate the comment to any language in the azure translator
    subscription_key = ""
    subscription_region = ""
    domain = ""
    
    # Set the headers for the request
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": subscription_region,
        "Content-Type": "application/json",
    }

    url = f"https://{domain}.cognitiveservices.azure.com/translator/text/v3.0/translate?to={lan}"

    # Set the JSON data to send in the request body
    data = json.dumps([{"Text": comment}])

    # Send the POST request
    response_tanslate = requests.post(url, headers=headers, data=data)
    return json.loads(response_tanslate.text)[0]["translations"][0]["text"]


def get_json_data():
    # connect to the blob and download the files
    connect_str = ""
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "story"
    container_client = blob_service_client.get_container_client(container_name)

    # download the json file
    streamdownloader = container_client.get_blob_client("story.json").download_blob()
    data_story = json.loads(streamdownloader.readall())

    # download the npz file
    streamdownloader = container_client.get_blob_client("dic_np.npz").download_blob()
    loaded_dict = np.load(io.BytesIO(streamdownloader.readall()))
    return loaded_dict, data_story


def app():
    # set a title for your app
    title_translate = "Green Eyes - Lonely Trees"
    st.title(title_translate)
    # start a form
    form = st.form(key="my_form")
    with form:
        # Add a input box and button
        enter_txt_he = st.text_input(label="", key="qustion")
        submit_button = st.form_submit_button(label="Find me the quotes")
        if submit_button:
            # load the data
            loaded_dict, data_story = get_json_data()
            # get the matrix embedding
            matrix_embedding = np.array([loaded_dict[key] for key in loaded_dict])
            # get the question in english
            enter_txt_en = get_lan(enter_txt_he, lan="en")

            # get the question embedding
            embedding = openai.Embedding.create(
                input=enter_txt_en, engine="text-embedding-ada-002"
            )["data"][0]["embedding"]

            # calculate the cosine similarity
            cosine_vector = np.dot(matrix_embedding, embedding) / (
                np.linalg.norm(matrix_embedding) * np.linalg.norm(embedding)
            )
            # get the index of the most similar quote
            idx_answer = np.argmax(cosine_vector)
            # get the answer in the original language (hebrew)
            answer = data_story[idx_answer]["text_he"]
            # print there answer
            st.write(answer)


app()
