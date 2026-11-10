# BuildingBot – Organizational Knowledge Chatbot

## Project

BuildingBot is a Hebrew chatbot designed to answer questions about organizational documents related to building management.

The project implements a Retrieval-Augmented Generation (RAG) architecture using LlamaIndex, ChromaDB, and OpenAI.

The goal is to generate answers based only on information retrieved from the organization's documents.

The project also includes a free demonstration mode that can run without an OpenAI API subscription.

## Technologies

- Python
- LlamaIndex
- ChromaDB
- OpenAI API
- Streamlit
- python-dotenv

## Design Decisions

### 1. Vector Database

**Choice:** ChromaDB with persistent local storage.

**Reason:** ChromaDB is lightweight, easy to use, integrates with LlamaIndex, and was introduced during the course.

### 2. LlamaIndex

**Choice:** LlamaIndex for the RAG pipeline.

**Reason:** It provides tools for document loading, chunking, embedding generation, indexing, and retrieval.

### 3. Document Chunking

**Choice:** SentenceSplitter with a chunk size of 512 tokens.

**Reason:** This approach considers sentence boundaries while limiting the amount of text in each chunk.

### 4. Chunk Overlap

**Choice:** 50 tokens.

**Reason:** Overlap helps preserve context when relevant information appears near chunk boundaries.

### 5. API Provider

**Choice:** OpenAI API.

**Reason:** OpenAI provides embedding and language models that integrate with LlamaIndex.

### 6. Top K

**Choice:** Top K = 3.

**Reason:** Retrieving three relevant chunks provides a balance between useful context, response time, and API cost.

### 7. Models

**Embedding model:** `text-embedding-3-small`

**Answer generation model:** `gpt-4.1-mini`

**Reason:** These models were selected with consideration for cost, functionality, and integration with LlamaIndex.

### 8. Query Expansion

**Choice:** Disabled.

**Reason:** Query expansion requires additional processing and potentially additional API calls. For this small project, direct semantic retrieval was selected.

### 9. Search Method

**Choice:** Semantic vector search using cosine similarity in ChromaDB.

**Reason:** Semantic search can retrieve relevant document chunks even when the user's question does not use exactly the same words as the documents.

An initial similarity threshold of 0.5 was considered during development. This value requires empirical testing and tuning; its use in the current implementation is not confirmed.

## System Workflow

1. Load organizational documents from the `documents` directory.
2. Split documents into chunks using LlamaIndex.
3. Generate embeddings for each chunk.
4. Store embeddings in ChromaDB.
5. Receive a user question through Streamlit.
6. Generate an embedding for the question.
7. Retrieve the top three relevant chunks.
8. Send the retrieved context and question to the language model.
9. Generate an answer in Hebrew.
10. Display the answer and source filenames.

## Running the Project

### Installation

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Demo Mode – Free

Run:

```powershell
python -m streamlit run app.py
```

Open:

`http://localhost:8501`

Select **הדגמה חינמית**.

Demo mode uses predefined answers based on the sample documents. It does not perform actual vector retrieval or call an AI model.

### Real RAG Mode – OpenAI

1. Copy `.env.example` to `.env`.
2. Add a valid OpenAI API key with available credits.
3. Run:

```powershell
python ingest.py
```

4. Start the application:

```powershell
python -m streamlit run app.py
```

5. Select **RAG אמיתי - OpenAI**.

**Note:** The complete RAG workflow has not yet been successfully tested because the OpenAI API account had no available credits.

## Testing

The Streamlit application was launched successfully, and the demonstration mode was tested.

Example questions:

- How much is the monthly building committee fee?
- When must the fee be paid?
- On which days is the staircase cleaned?
- Who should be contacted about an elevator malfunction?
- What are the building's quiet hours?

The real RAG mode still requires end-to-end testing with an active API account.

## Three Real Development Problems

### Problem 1 – Missing config.py File

**Observed error:**

`ModuleNotFoundError: No module named 'config'`

**Investigation:**

While running `python ingest.py`, Python could not import the `config` module.

I executed:

`dir config*`

The command returned no matching files, confirming that `config.py` was missing from the project directory.

**Solution:**

I created `config.py` and added the project configuration, including model names, document paths, chunk size, overlap, and Top K.

After this change, the ingestion process advanced to the embedding generation stage.

**Status:** Resolved.

### Problem 2 – Import Error Between rag.py and ingest.py

**Observed error:**

`ImportError: cannot import name 'get_collection' from 'ingest'`

**Investigation:**

The `rag.py` file attempted to import `get_collection` and `get_embedding` from `ingest.py`, but these functions were not defined there.

The error was caused by inconsistent code versions.

**Solution:**

I updated `rag.py` to initialize the ChromaDB connection and embedding model using the project's configuration, removing the invalid imports.

After updating the file, the Streamlit application started successfully.

**Status:** Resolved.

### Problem 3 – OpenAI API Credit Error

**Observed error:**

`RateLimitError: 429`

`credit_balance_exhausted`

**Investigation:**

During the execution of `python ingest.py`, document transformations completed successfully, but the embedding generation process failed.

The OpenAI API response indicated that no credits were available.

**Solution:**

I added a free demonstration mode to allow the application interface to be tested without paid API calls.

I created `demo.py` with predefined answers based on the sample documents and updated `app.py` to support switching between demo mode and real RAG mode.

**Status:** The demonstration mode works. The API credit issue remains unresolved, and the real RAG pipeline has not yet been verified end to end.

## Limitations

- The real RAG mode requires OpenAI API credits.
- The complete RAG pipeline has not been successfully tested.
- Demo mode uses predefined answers and keyword matching, not semantic retrieval.
- Similarity thresholds require empirical tuning.
- The language model is instructed to use organizational documents only, but this does not guarantee that every answer is fully grounded.
- Source filenames indicate retrieved documents, not necessarily verified evidence for each generated statement.
- Documents must be re-indexed after changes.

## Security

The OpenAI API key is stored locally in `.env`.

The `.gitignore` file excludes `.env`, the virtual environment, and generated database files.

API keys must never be committed to GitHub.