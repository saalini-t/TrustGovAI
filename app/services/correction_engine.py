def correct_answer(query, context):
    """Simple correction by extracting from context"""
    # For hackathon: Use context directly instead of heavy LLM
    # This ensures fast correction without loading Mistral
    
    # Return first 200 chars of context as corrected answer
    corrected = context.split("\n")[0] if context else "Please refer to official government sources."
    
    return corrected