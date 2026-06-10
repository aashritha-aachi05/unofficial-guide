# The Unofficial Guide: Rutgers CS Professor Reviews

A Retrieval-Augmented Generation (RAG) system that answers questions about
Rutgers University Computer Science professors, grounded in real student reviews.

Official university channels only list course descriptions and professor names —
they don't tell you which professors give useful feedback, which exams are curved,
or whose teaching style actually helps. Students rely on word-of-mouth and Rate My
Professors, but there's no way to search across all of it at once. This project
makes those reviews searchable and answerable in plain language.

## How it works

```
Documents (.txt reviews)
        ↓  ingest.py
Clean + chunk (300-char chunks, 50-char overlap)
        ↓  embed.py
Embed (sentence-transformers: all-MiniLM-L6-v2)  →  Vector store (ChromaDB)
        ↓  query.py
Retrieve top-5 chunks  →  Generate grounded answer (Groq: llama-3.3-70b-versatile)
        ↓  app.py
Gradio web interface
```

The generator is constrained to answer **only** from the retrieved reviews — it
won't invent ratings, courses, or opinions, and it says so when the reviews don't
cover a question.

## Project structure

| File | Purpose |
|------|---------|
| `ingest.py` | Loads `.txt` files from `documents/`, cleans whitespace, and chunks them. |
| `embed.py` | Embeds chunks with `all-MiniLM-L6-v2` and stores them in ChromaDB; exposes `retrieve()`. |
| `query.py` | Retrieves relevant reviews and generates a grounded answer via Groq. |
| `app.py` | Gradio web interface over the pipeline. |
| `documents/` | One `.txt` file per professor, with reviews copied from Rate My Professors. |
| `planning.md` | Design notes: chunking strategy, retrieval approach, evaluation plan. |

## Setup

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Add your Groq API key to a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_key_here
   ```

   Get a free key at <https://console.groq.com>.

## Usage

Run the steps in order. Each script can be run directly to inspect its output.

```bash
# 1. Preview chunks
python ingest.py

# 2. Build the vector store (creates ./chroma_db)
python embed.py

# 3. Ask a question from the command line
python query.py

# 4. Launch the web interface (http://127.0.0.1:7860)
python app.py
```

`embed.py` must be run at least once before `query.py` or `app.py`, since they
read from the ChromaDB index it builds. Re-run `embed.py` whenever you add or edit
reviews in `documents/`.

## Adding reviews

Each file in `documents/` follows this format:

```
Profesor: <Name>
Course: <CSxxx>
Rating: <n>/5
Review: <text>

Rating: <n>/5
Review: <text>
```

Add more `Rating:` / `Review:` pairs under a professor to include additional
reviews. After editing, re-run `python embed.py` to refresh the index.

## Tech stack

- **Embeddings:** [sentence-transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`) — free and runs locally
- **Vector store:** [ChromaDB](https://www.trychroma.com/)
- **Generation:** [Groq](https://groq.com/) (`llama-3.3-70b-versatile`)
- **Interface:** [Gradio](https://www.gradio.app/)
