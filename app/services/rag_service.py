from app.utils.vector_store import retrieve_documents
from transformers import pipeline

# Lazy load LLM to avoid startup issues
_generator = None

def _load_generator():
    global _generator
    if _generator is None:
        _generator = pipeline("text-generation", model="distilgpt2")
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
    """Generate answer using RAG with LLM"""
    context, sources = retrieve_context(query)
    
    generator = _load_generator()
    
    prompt = f"""Use the following government scheme information to answer.

Context:
{context}

Question:
{query}

Answer:"""
    
    result = generator(prompt, max_length=200, do_sample=False, truncation=True)
    answer = result[0]["generated_text"]
    
    # Extract only the answer part
    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()
    
    return answer, context, sources