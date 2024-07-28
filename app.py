import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

load_dotenv()

# Styling
page_bg = '''<style>
    [data-testid="stAppViewContainer"] {
    background-image: url('https://i.pinimg.com/564x/4e/aa/1c/4eaa1c3918fe7d76870cd0b24d4a78ad.jpg');
    background-size: cover;
    }
    [data-testid="stSidebar"]{
    background-image: url('https://i.pinimg.com/564x/93/bf/4b/93bf4bd22cf91f21c50edcd7ea2129fb.jpg');
    background-size: cover;
    }
    [data-testid="baseButton-secondary"]{
        background-color:#16660f;
        color:white;
    }
    .image-container {
        display: flex;
        justify-content: center;
    }
    .output-box {
        background-color: #ffffff;
        color: #000000;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        font-size: 16px;  /* Adjust font size as needed */
    }
    </style>'''
st.markdown(page_bg, unsafe_allow_html=True)

# BackEnd
# Defining Functionality Of The Application Using GoogleApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    try:
        # Initializing the vision pro model
        model = genai.GenerativeModel("gemini-1.5-pro")
        # Generating response by giving the image input
        response = model.generate_content([input_prompt, image[0]])
        # Returning the text output
        return response.text
    except Exception as e:
        st.error(f"Error in API call: {e}")
        return "Error occurred during API call."

def input_image_setup(uploaded_file=None, selected_image_url=None):
    try:
        if uploaded_file is not None:
            # Read the file into bytes
            byte_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": byte_data
                }
            ]
            return image_parts
        elif selected_image_url is not None:
            response = requests.get(selected_image_url)
            if response.status_code == 200:
                byte_data = response.content
                image_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": byte_data
                    }
                ]
                return image_parts
            else:
                st.error(f"Error fetching image from URL. Status code: {response.status_code}")
                return None
        else:
            raise FileNotFoundError("Invalid: No File Uploaded or Selected")
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# FrontEnd
# Initializing Streamlit Application

st.title("Gemini Nutrition Tracking App")
st.write("Upload an image of your food or select an image from the sidebar to get detailed information on calories")

# File upload
upload_file = st.file_uploader("Choose an image....", type=["jpg", "jpeg", "png"])

# Sidebar with predefined images
image_urls = [
    None,
    'https://i.pinimg.com/564x/b1/c5/96/b1c5966c316d50040c38e4d149315990.jpg',
    'https://www.holidify.com/images/cmsuploads/compressed/Bebek_Goreng_Malang_20190629115440.JPG',
    'https://i.pinimg.com/564x/c8/fb/b7/c8fbb7e6957170e15aaa3e08096ac345.jpg',
    'https://media.istockphoto.com/id/1190330112/photo/fried-pork-and-vegetables-on-white-background.jpg?s=612x612&w=0&k=20&c=TzvLLGGvPAmxhKJ6fz91UGek-zLNNCh4iq7MVWLnFwo=',
    'https://www.eatthis.com/wp-content/uploads/sites/4/2021/05/healthy-plate.jpg?quality=82&strip=1',
    'https://images.news18.com/ibnlive/uploads/2023/10/vegetarian-meal-2023-10-00fe64d614706b15c03a1e95c2ae6813.jpg'
    
]
image_options = ["None"]
image_options = [f'Image {i+1}' for i in range(1,len(image_urls))]


st.sidebar.header("Select an Image")
st.sidebar.write("Choose an image to test the model")

selected_image_url = st.sidebar.radio("Choose an image", image_urls, format_func=lambda url: f"Image {image_urls.index(url) + 1}")

# Display the uploaded or selected image
if upload_file is not None:
    image = Image.open(upload_file)
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.image(image, caption="Uploaded Image", use_column_width=False, width=300)
    st.markdown('</div>', unsafe_allow_html=True)
    image_data = input_image_setup(uploaded_file=upload_file)
elif selected_image_url is not None:
    image_data = input_image_setup(selected_image_url=selected_image_url)
    if image_data:
        response = requests.get(selected_image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.markdown('<div class="image-container">', unsafe_allow_html=True)
            st.image(image, caption=f"Selected Image: Image {image_urls.index(selected_image_url) + 1}", use_column_width=False, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(f"Failed to load the selected image from URL.")
    else:
        st.error(f"No image data available for selected image.")
else:
    st.write("No Image was Uploaded or Selected")
    image_data = None

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image,
DO NOT GIVE ANSWERS LIKE "it is impossible"
and calculate the total calories, also provide the details of every food item with calories intake
in the below format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----
"""

# To add functionality to the button to deliver a response
if submit:
    if image_data:
        # Get the response
        response = get_gemini_response(input_prompt, image_data)
        
        # Display the response in a styled box with black text
        st.subheader("The Response is")
        st.markdown(f'<div class="output-box">{response}</div>', unsafe_allow_html=True)
    else:
        st.error("No image data available. Please upload or select an image.")
