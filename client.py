import streamlit as st
import os

st.set_page_config(page_title="Embed a.html", layout="wide")
st.title("Embedding a.html in Streamlit")

# Read the content of `a.html`
html_file_path = os.path.join("static", "uploader.html")
with open(html_file_path, "r") as f:
    html_content = f.read()

# Render the HTML in Streamlit
st.components.v1.html(html_content, height=200)
# Listen for messages from JavaScript (via postMessage)
def listen_for_data():
    # Streamlit won't directly expose JavaScript variables, so we use `st.experimental_get_query_params()`
    message = st.experimental_get_query_params()
    if 'outputData' in message:
        return message['outputData'][0]  # Capture the `outputData`
    return None

# Capture the output data (sent via postMessage)
output_data = listen_for_data()

if output_data:
    # Display the processed data in Streamlit
    output_placeholder.text(f"Processed Data:\n{output_data}")
