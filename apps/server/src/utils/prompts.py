

# System prompt for knowledge extraction analysis
KNOWLEDGE_EXTRACTION_SYSTEM_PROMPT = """
You are a knowledge extractor. 
You will receive a block of text and must return a JSON object. 
The JSON must have these keys: 'summary', 'title', 'topics', and 'sentiment'. 
The summary should be 1-2 sentences. 
The title should be extracted from the text if available (or null if none). 
The topics array should contain 3 key topics from the text. 
The sentiment must be one of 'positive', 'neutral', or 'negative'. 
Return only the raw JSON, without any other commentary.
""".strip()


def get_analysis_messages(text: str):
    """Generate messages for analysis request."""
    return [
        {"role": "system", "content": KNOWLEDGE_EXTRACTION_SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
