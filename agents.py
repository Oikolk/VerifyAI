import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

load_dotenv()

# Configure the client
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_ID = "gemini-2.5-flash"

def researcher_agent(claim):
    """
    Uses Google Search Grounding to find information about the claim.
    """
    print(f"Researcher Agent: Searching for '{claim}'...")
    
    prompt = f"""
    Research the following claim extensively using Google Search. 
    Claim: "{claim}"
    
    Gather facts, dates, and credible sources that support or refute this claim.
    Return a detailed summary of the findings.
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                response_modalities=["TEXT"]
            )
        )
        
        # Extract grounding metadata if available
        grounding_metadata = response.candidates[0].grounding_metadata
        
        return {
            "text": response.text,
            "grounding_metadata": grounding_metadata
        }
    except Exception as e:
        return {"error": str(e)}

def analyst_agent(claim, research_data):
    """
    Analyzes the research data to extract core facts.
    """
    print("Analyst Agent: Analyzing research data...")
    
    if "error" in research_data:
        return {"error": research_data["error"]}

    prompt = f"""
    You are an expert Analyst. Analyze the following research data regarding the claim: "{claim}".
    
    Research Data:
    {research_data['text']}
    
    Identify the key facts, contradictions, and the credibility of the sources.
    Filter out irrelevant information.
    Provide a structured analysis.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    
    return response.text

def judge_agent(claim, analysis):
    """
    Makes a final verdict based on the analysis.
    """
    print("Judge Agent: Deliberating...")
    
    prompt = f"""
    You are the Judge. Based on the following analysis of the claim "{claim}", determine if the claim is TRUE, FALSE, or UNVERIFIED.
    
    Analysis:
    {analysis}
    
    Provide:
    1. Verdict (TRUE, FALSE, or UNVERIFIED)
    2. Confidence Score (0-100%)
    3. A concise summary explaining the verdict.
    
    Return the result as a JSON object with keys: "verdict", "confidence", "summary".
    Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "verdict": "ERROR",
            "confidence": 0,
            "summary": "Failed to parse Judge's response."
        }
