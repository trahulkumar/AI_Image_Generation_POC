# ✨ AI Image Generator Dashboard

A professional, cloud-ready AI Image Generation application built with **Streamlit** and the **Hugging Face Inference API**.

![App Screenshot](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

## 🚀 Features

-   **State-of-the-Art Models**: Access top-tier text-to-image models without needing a GPU:
    -   **FLUX.1-schnell**: The fastest and highest quality open model.
    -   **Stable Diffusion XL 1.0**: Reliable, high-resolution generation.
-   **Cloud Ready**: Runs entirely on CPU by leveraging the Hugging Face Inference API.
-   **Smart Fallback**: Automatically switches between `InferenceClient` and raw API requests to ensure reliability across different models.
-   **Modern UI**: Redesigned interface inspired by premium dashboards, featuring:
    -   Centralized configuration.
    -   Persistent session state (images don't disappear).
    -   Visual feedback and error handling.
-   **Secure**: No hardcoded secrets.

## 🛠️ Prerequisites

-   **Python 3.8+**
-   **Hugging Face Access Token**: You need a free token with "Read" permissions. [Get it here](https://huggingface.co/settings/tokens).

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/trahulkumar/AI_Image_Generation_POC.git
    cd AI_Image_Generation_POC
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ How to Run

1.  Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2.  Open your browser at `http://localhost:8501`.

3.  **Configure**:
    -   Paste your **Hugging Face Token** in the "Configuration" box.
    -   Select your desired **Model**.

4.  **Generate**:
    -   Enter a prompt (e.g., *"A cyberpunk city at night, neon lights, 8k, realistic"*).
    -   Click **🚀 Generate Image**.

## 🧩 Project Structure

-   `app.py`: Main Streamlit application file containing UI and logic.
-   `requirements.txt`: List of Python dependencies.
-   `backend/`: (Legacy) FastAPI backend from initial POC.
-   `frontend/`: (Legacy) HTML/JS frontend from initial POC.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
