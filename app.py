import streamlit as st
from pathlib import Path
import google.generativeai as genai
from google_api_key import google_api_key
import os
google_api_key = os.getenv('google_api_key')
# Configure API
genai.configure(api_key=google_api_key)

# AI Model Configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System Prompt
system_prompts = [
    """
    You are a domain expert in veterinary medicine. You are tasked with 
    examining images of pets to identify diseases, injuries, or any health issues.
    
    Your key responsibilities:
    1. Detailed Analysis: Thoroughly examine each image, focusing on finding any abnormalities.
    2. Analysis Report: Document all findings and articulate them in a structured format.
    3. Recommendations: Based on the analysis, suggest remedies, treatments, or preventive measures.
    
    Important Notes:
    1. Scope of response: Only respond if the image pertains to pet health issues.
    2. Clarity of image: If the image is unclear, note that certain aspects are 
    'Unable to be correctly determined based on the uploaded image'.
    3. Disclaimer: Accompany your analysis with the disclaimer: 
    "Consult with a veterinarian before making any decisions."
    4. Your insights are invaluable in guiding decisions related to pet health. 
    Please proceed with the analysis, adhering to the structured approach outlined above.
    
    Provide the final response with these headings: 
    Detailed Analysis, Analysis Report, Recommendations
    """
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit App
st.set_page_config(page_title="Pet Disease Identifier", page_icon="🐾", layout="wide")
st.title("Pet Disease Identifier 🐶 🐱 🐰")
st.subheader("An app to help with pet disease analysis using images")

file_uploaded = st.file_uploader('Upload the pet image for Analysis', type=['png', 'jpg', 'jpeg'])

if file_uploaded:
    st.image(file_uploaded, width=200, caption='Uploaded Image')
    
submit = st.button("Generate Analysis")

if submit:
    image_data = file_uploaded.getvalue()
    
    image_parts = [
        {
            "mime_type": "image/jpg",
            "data": image_data
        }
    ]
    
    # Prepare prompt
    prompt_parts = [
        image_parts[0],
        system_prompts[0],
    ]
    
    # Generate response
    response = model.generate_content(prompt_parts)
    if response:
        st.title('Detailed analysis based on the uploaded image')
        st.write(response.text)
