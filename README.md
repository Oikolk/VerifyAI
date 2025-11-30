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

## System Architecture
![System Architecture Workflow](WORKFLOW.png)
The VerifyAI pipeline follows a linear multi-agent workflow orchestrated by Streamlit:

1. **User Input**: The user submits a claim via the web interface.

2. **Cache Check**: The system first checks the SessionState cache to see if this specific claim has already been verified to save resources.

3. **Agent 1: The Researcher**: If not cached, the claim is passed to the Researcher. This agent utilizes the Google Search Grounding tool (via google-genai SDK) to perform live web searches, returning raw text and grounding metadata (source URLs).

4. **Agent 2: The Analyst**: This agent acts as a filter. It ingests the raw research data, evaluates the credibility of the sources, and extracts only the factual evidence relevant to the claim.

5. **Agent 3: The Judge**: The final decision-maker. It reviews the Analyst's structured report and produces a final JSON object containing the Verdict (TRUE/FALSE/UNVERIFIED), a Confidence Score, and a user-friendly Summary.

6. **Output**: The Streamlit UI parses the JSON and renders the verdict card along with clickable source citations.
