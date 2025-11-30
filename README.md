# VerifyAI - The Agentic Truth Shield

## Setup

1.  **API Key**: Open `.env` and replace `your_api_key_here` with your actual Google GenAI API Key.
    ```env
    GOOGLE_API_KEY=AIzaSy...
    ```

2.  **Run the App**:
    ```bash
    streamlit run main.py
    ```

## Features
- **Researcher Agent**: Searches the web using Google Search Grounding.
- **Analyst Agent**: Filters and analyzes the data.
- **Judge Agent**: Delivers a final verdict with a confidence score.
- **Caching**: Remembers previously verified claims.
