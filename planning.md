## Domain
Student reviews of Rutgers University Computer Science professors. This 
knowledge is valuable because 
official university channels only provide basic course descriptions and 
professor names — they don't 
tell students which professors give useful feedback, which exams are 
curved, or which teaching styles 
actually help students learn. Students rely on word-of-mouth and platforms 
like Rate My Professors 
but there's no way to search across all of it at once.

## Documents
- documents/sesh_venugopal.txt — RMP reviews for Sesh Venugopal (CS112)
- documents/david_menendez.txt — RMP reviews for David Menendez (CS314)
- documents/hao_wang.txt — RMP reviews for Hao Wang
- documents/abraham_gale.txt — RMP reviews for Abraham Gale (CS205)
- documents/ananda_gunawardena.txt — RMP reviews for Ananda Gunawardena
- documents/bernhard_firner.txt — RMP reviews for Bernhard Firner
- documents/lily_chang.txt — RMP reviews for Lily Chang
- documents/minesh_patel.txt — RMP reviews for Minesh Patel
- documents/paula_contento.txt — RMP reviews for Paula Contento
- documents/samaneh_hamidi.txt — RMP reviews for Samaneh Hamidi

## Chunking Strategy
Chunk size: 300 characters, overlap: 50 characters. RMP reviews are short 
and opinion-dense — 
each review is typically 2-4 sentences covering one specific aspect 
(exams, grading, teaching style). 
A 300-character chunk captures one full review without merging unrelated 
opinions from different 
students. The 50-character overlap ensures that if a key opinion spans a 
sentence boundary it won't 
get cut off entirely.

## Retrieval Approach
Embedding model: all-MiniLM-L6-v2 via sentence-transformers. Top-k: 5 
chunks per query. 
For a production system I would weigh: cost (all-MiniLM-L6-v2 is free and 
local vs. OpenAI 
embeddings which cost per token), context length (some models handle 
longer text better), 
and accuracy on domain-specific informal text. all-MiniLM-L6-v2 is a good 
fit here because 
reviews are short and informal.

## Evaluation Plan
1. What do students say about Sesh Venugopal's exams?
   Expected: Reviews mention exams are based on lecture material, may 
mention curves.

2. Which professor is best for CS112 Data Structures?
   Expected: System returns reviews comparing professors who teach CS112.

3. Does Abraham Gale curve grades in CS205?
   Expected: Reviews mention whether grading is curved or strict.

4. What do students say about Bernhard Firner's teaching style?
   Expected: Reviews describe lecture quality, clarity, pace.

5. Which CS professor gives the most useful feedback on assignments?
   Expected: Reviews mentioning feedback quality on homework or projects.

## Anticipated Challenges
1. Reviews are very short — some are only 1-2 sentences. Chunks may be too 
small to carry 
   enough semantic signal, causing retrieval to return loosely related 
results.
2. Students sometimes refer to professors by last name only or nicknames — 
the embedding model 
   may not match "Sesh" to "Sesh Venugopal" correctly, causing missed 
retrievals.

## AI Tool Plan
1. Chunking + ingestion code: I'll share my Documents and Chunking 
Strategy sections with Claude 
   and ask it to implement ingest.py — a script that loads .txt files, 
cleans them, and chunks 
   them at 300 characters with 50-character overlap.
2. Embedding + retrieval code: I'll share my Retrieval Approach section 
and ask Claude to implement 
   embed.py that embeds chunks with all-MiniLM-L6-v2 and stores them in 
ChromaDB, plus a 
   retrieve() function that takes a query and returns top-5 chunks with 
source filenames.
3. Generation + interface: I'll share my grounding requirement and ask 
Claude to implement 
   query.py with a Groq-backed generate() function and app.py with a 
Gradio interface.

## Architecture
Document Ingestion (.txt files)
        ↓
Cleaning + Chunking (Python, 300 char chunks, 50 overlap)
        ↓
Embedding (sentence-transformers: all-MiniLM-L6-v2)
        ↓
Vector Store (ChromaDB)
        ↓
Retrieval (top-5 semantic search)
        ↓
Generation (Groq: llama-3.3-70b-versatile)
        ↓
Gradio Interface
