from app.utils.vector_store import retrieve_documents
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import os

# Lazy load LLM to avoid startup issues
_generator = None
_tokenizer = None

# Check if we should use fast mode (no LLM, just retrieval)
FAST_MODE = os.environ.get("FAST_MODE", "true").lower() == "true"

def _load_generator():
    global _generator, _tokenizer
    if _generator is None:
        print("🔄 Loading LLM model (one-time)...")
        # Use smaller, faster model with optimizations
        model_name = "distilgpt2"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        _generator = pipeline(
            "text-generation", 
            model=model,
            tokenizer=_tokenizer,
            device=-1  # CPU
        )
        print("✅ LLM model loaded!")
    return _generator


def retrieve_context(query):
    """Retrieve context documents and their sources"""
    docs = retrieve_documents(query, k=3)
    
    context = ""
    sources = []
    
    for d in docs:
        context += d["text"] + "\n"
        sources.append(d["source"])
    
    return context, sources


def generate_rag_answer(query):
    """Generate answer using RAG - Fast mode uses retrieval only"""
    context, sources = retrieve_context(query)
    
    if FAST_MODE:
        # Fast mode: Return the most relevant context directly
        # This is much faster and often more accurate for factual Q&A
        answer = context.strip().split('\n')[0]  # Return first relevant chunk
        if len(answer) < 20:
            answer = context.strip()[:300]
        return answer, context, sources
    
    # Slow mode: Use LLM for generation
    generator = _load_generator()
    
    # Shorter, more focused prompt for faster generation
    prompt = f"""Context: {context[:500]}

Q: {query}
A:"""
    
    result = generator(
        prompt, 
        max_new_tokens=80,  # Reduced for speed
        do_sample=False, 
        truncation=True,
        pad_token_id=generator.tokenizer.eos_token_id
    )
    answer = result[0]["generated_text"]
    
    # Extract only the answer part
    if "A:" in answer:
        answer = answer.split("A:")[-1].strip()
    
    # Clean up the answer (stop at newlines or repetition)
    answer = answer.split("\n")[0].strip()
    
    return answer, context, sources