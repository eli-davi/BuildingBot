# BuildingBot – Organizational Knowledge Chatbot

## Project
A Hebrew RAG chatbot for building management documents.

## Technologies
Python, LlamaIndex, ChromaDB, OpenAI and Streamlit.

## Design decisions
- Vector DB: ChromaDB, persistent local storage.
- Chunking: 512 tokens, overlap 50.
- Retrieval: semantic vector search, Top K = 3.
- Embeddings: text-embedding-3-small.
- Answer model: gpt-4.1-mini.
- Query expansion: disabled to reduce cost.
- Similarity threshold: initial experimental value 0.5.

## Run
1. Install requirements.
2. Copy .env.example to .env and configure the API key.
3. Run python ingest.py.
4. Run streamlit run app.py.

## Testing
Check questions that are answered in the documents,
questions that are not answered, and paraphrased questions.

## Three real development problems
Complete after testing:
1. Problem, observed error, investigation, solution.
2. Problem, observed error, investigation, solution.
3. Problem, observed error, investigation, solution.

## Limitations
Similarity thresholds require empirical tuning.
The chatbot is instructed to use documents only,
but LLM answers are not mathematically guaranteed.
Source filenames identify retrieved material,
not necessarily verified supporting evidence.
Re-run ingestion after changing documents.
