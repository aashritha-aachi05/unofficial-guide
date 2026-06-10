"""Answer questions about Rutgers CS professors, grounded in retrieved reviews.

Retrieval: top-5 chunks from ChromaDB (see embed.py).
Generation: Groq's llama-3.3-70b-versatile, constrained to the retrieved text.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve, TOP_K

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = (
    "You answer questions about Rutgers University Computer Science professors "
    "using ONLY the student reviews provided in the context. "
    "Do not use outside knowledge or invent ratings, courses, or opinions. "
    "If the context does not contain enough information to answer, say so plainly. "
    "When helpful, attribute opinions to the professor they describe and note when "
    "students disagree. Keep answers concise and grounded in the reviews."
)


def _format_context(chunks):
    """Render retrieved chunks into a numbered context block for the prompt."""
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        blocks.append(f"[{i}] (source: {chunk['source']})\n{chunk['text']}")
    return "\n\n".join(blocks)


def generate(query, k=TOP_K):
    """Retrieve relevant reviews and generate a grounded answer.

    Returns a dict: {"answer": str, "sources": [filenames], "chunks": [...]}.
    """
    chunks = retrieve(query, k=k)
    context = _format_context(chunks)

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Context (student reviews):\n\n{context}\n\n"
                    f"Question: {query}"
                ),
            },
        ],
        temperature=0.2,
    )
    answer = response.choices[0].message.content

    # De-duplicated source filenames, preserving retrieval order.
    sources = list(dict.fromkeys(c["source"] for c in chunks))
    return {"answer": answer, "sources": sources, "chunks": chunks}


if __name__ == "__main__":
    sample_query = "What do students say about Sesh Venugopal's exams?"
    print(f"Question: {sample_query}\n")
    result = generate(sample_query)
    print("Answer:")
    print(result["answer"])
    print("\nSources:", ", ".join(result["sources"]))
