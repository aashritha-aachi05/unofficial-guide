"""Gradio interface for the Rutgers CS professor review RAG system.

Ask a question -> retrieve relevant reviews -> generate a grounded answer.
Run with:  python app.py
"""

import gradio as gr

from query import generate

EXAMPLE_QUESTIONS = [
    "What do students say about Sesh Venugopal's exams?",
    "Which professor is best for CS112 Data Structures?",
    "Does Abraham Gale curve grades in CS205?",
    "What do students say about Bernhard Firner's teaching style?",
    "Which CS professor gives the most useful feedback on assignments?",
]


def answer_question(query):
    """Run a query through the RAG pipeline and return answer + sources text."""
    if not query or not query.strip():
        return "Please enter a question.", ""
    result = generate(query)
    sources = "\n".join(f"- {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="Rutgers CS Professor Reviews") as demo:
    gr.Markdown(
        "# Rutgers CS Professor Reviews\n"
        "Ask about Rutgers Computer Science professors. Answers are grounded "
        "in student reviews — the system won't make up ratings or opinions."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="e.g. Does Abraham Gale curve grades in CS205?",
        lines=2,
    )
    ask_btn = gr.Button("Ask", variant="primary")

    answer = gr.Textbox(label="Answer", lines=6)
    sources = gr.Textbox(label="Sources (retrieved reviews)", lines=5)

    # run_on_click runs the query when an example is clicked (instead of only
    # filling the textbox), so the Answer/Sources boxes refresh every time.
    # cache_examples=False keeps each click a live query rather than a snapshot.
    gr.Examples(
        examples=EXAMPLE_QUESTIONS,
        inputs=question,
        outputs=[answer, sources],
        fn=answer_question,
        run_on_click=True,
        cache_examples=False,
    )

    ask_btn.click(fn=answer_question, inputs=question, outputs=[answer, sources])
    question.submit(fn=answer_question, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch(share=True)
