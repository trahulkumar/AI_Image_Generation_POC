import streamlit as st
import requests
from huggingface_hub import InferenceClient
import io
from PIL import Image

# Page config
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 4px;
        height: 3rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        color: white;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 4px;
    }
    /* Style for the configuration container */
    div[data-testid="stExpander"] {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        background-color: #ffffff;
    }
    /* Reduce top padding */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Models
MODELS = {
    "1. FLUX.1-schnell (Fastest & Best Quality)": "black-forest-labs/FLUX.1-schnell",
    "2. Stable Diffusion XL 1.0 (High Quality)": "stabilityai/stable-diffusion-xl-base-1.0",
}

# Sidebar - Instructions
with st.sidebar:
    st.markdown("### 📖 How to use")
    st.markdown("""
    1. **Enter API Key**: Enter your Hugging Face Access Token in the Configuration section.
    2. **Select Model**: Choose a model from the dropdown.
    3. **Provide Prompt**:
        - Enter a detailed description of the image you want to generate.
    4. **Generate**: Click '🚀 Generate Image'.
    5. **Download**: Save your creation!
    """)
    st.markdown("---")
    st.markdown("[Get a free HF Token](https://huggingface.co/settings/tokens)")

# Main Content
st.title("✨ AI Image Generator Dashboard")
st.markdown("Create stunning visuals with AI-powered models.")

# Configuration Section
with st.expander("🔧 Configuration", expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        api_token = st.text_input("Hugging Face Token", type="password", help="Get your free token at huggingface.co/settings/tokens")
    with col2:
        selected_model_name = st.selectbox("Select Model", list(MODELS.keys()))
        model_id = MODELS[selected_model_name]

# Initialize session state
if "last_image" not in st.session_state:
    st.session_state.last_image = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# Input Section
st.markdown("### Enter Prompt")
prompt = st.text_area("Describe your image...", height=150, placeholder="A futuristic cityscape at sunset, 8k, photorealistic...")

# Generate Button
generate_btn = st.button("🚀 Generate Image")

# Logic
if generate_btn:
    if not api_token:
        st.error("Please enter your Hugging Face API Token in the Configuration section.")
    elif not prompt:
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Generating image..."):
            try:
                # Initialize client
                client = InferenceClient(token=api_token)
                
                # Try Method 1: InferenceClient
                try:
                    image = client.text_to_image(prompt, model=model_id)
                except Exception as client_error:
                    # Try Method 2: Raw Router API (Fallback)
                    API_URL = f"https://router.huggingface.co/models/{model_id}"
                    headers = {"Authorization": f"Bearer {api_token}"}
                    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
                    
                    if response.status_code != 200:
                        raise Exception(f"API Error: {response.status_code} - {response.text}")
                        
                    image = Image.open(io.BytesIO(response.content))

                # Save to session state
                st.session_state.last_image = image
                st.session_state.last_prompt = prompt
                st.success("Image generated successfully!")
                
            except Exception as e:
                st.error("Error generating image.")
                st.error(f"Details: {e}")
                if "402" in str(e):
                    st.warning("⚠️ This model requires Hugging Face Pro/Enterprise credits. Please try 'Stable Diffusion XL' or 'FLUX.1-schnell' instead.")
                elif "401" in str(e):
                    st.warning("⚠️ Authentication failed. Please check your token.")

# Display Image from Session State
if st.session_state.last_image:
    st.image(st.session_state.last_image, caption=st.session_state.last_prompt, use_container_width=True)
    
    # Download button
    buf = io.BytesIO()
    st.session_state.last_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="generated_image.png",
        mime="image/png"
    )
