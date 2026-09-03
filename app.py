"""The Unofficial Guide -- Streamlit interface (stage 5 of the pipeline).

Wires the whole pipeline together for a user:

    question -> retrieval.retrieve()  (all-MiniLM-L6-v2 + ChromaDB, top-k)
             -> generate.answer_question()  (gpt-oss-120b, grounded)
             -> answer + source list + the passages it was allowed to use

Run it:
    streamlit run app.py

Expects `python ingest.py` and `python retrieval.py --build` to have been run
first; the sidebar says so if the index is missing.
"""

import streamlit as st

from generate import MIN_SIMILARITY, MODEL, answer_question
from retrieval import EMBEDDING_MODEL, EVAL_QUESTIONS, TOP_K, get_collection

st.set_page_config(page_title="The Unofficial Curly Girl Guide", page_icon="💖", layout="centered")

# Topic label for each of the 5 questions in EVAL_QUESTIONS, in the same order.
# Buttons are narrow, so these name the subject instead of quoting the question.
TOPIC_LABELS = [
    "4C hair care",
    "Length retention",
    "Workout hair",
    "Heat damage",
    "Porosity",
]
assert len(TOPIC_LABELS) == len(EVAL_QUESTIONS), "one label per test question"

# Palette lives in .streamlit/config.toml; this styles the pieces the theme
# config can't reach (gradient heading, pill buttons, card-style expanders).
st.markdown(
    """
    <style>
      :root {
        --pink-deep: #C42A66;
        --pink: #E5397F;
        --pink-soft: #FDE8F1;
        --pink-line: #F5C2D8;
      }
      /* Gradient wordmark for the page title. */
      h1 {
        background: linear-gradient(95deg, #E5397F 0%, #B84FC7 55%, #7C5CE0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
      }
      h3 { color: var(--pink-deep) !important; }

      /* Rounded pink buttons, filled for the primary "Ask". */
      .stButton > button {
        border-radius: 999px;
        border: 1px solid var(--pink-line);
        background: #FFFFFF;
        color: var(--pink-deep);
        font-weight: 600;
        transition: all 0.15s ease;
      }
      .stButton > button:hover {
        border-color: var(--pink);
        background: var(--pink-soft);
        transform: translateY(-1px);
      }
      .stButton > button[kind="primary"] {
        background: linear-gradient(95deg, #E5397F, #B84FC7);
        border: none;
        color: #FFFFFF;
        box-shadow: 0 4px 14px rgba(229, 57, 127, 0.30);
      }

      /* Soft cards for the input and the retrieved-passages expander. */
      .stTextInput input {
        border-radius: 14px;
        border: 1.5px solid var(--pink-line);
        background: #FFFFFF;
        padding: 0.6rem 0.9rem;
      }
      .stTextInput input:focus { border-color: var(--pink); }
      div[data-testid="stExpander"] {
        border: 1px solid var(--pink-line);
        border-radius: 16px;
        background: #FFFFFF;
        overflow: hidden;
      }
      hr { border-color: var(--pink-line) !important; }

      /* Sidebar reads as a panel rather than a second page. */
      section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FDE8F1 0%, #F3E4FA 100%);
        border-right: 1px solid var(--pink-line);
      }
      section[data-testid="stSidebar"] h2 { color: var(--pink-deep); }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def load_collection():
    """Open ChromaDB once and reuse it across reruns."""
    return get_collection()


def render_sources(result) -> None:
    st.markdown("**Sources**")
    for i, (title, url) in enumerate(result.source_documents, start=1):
        st.markdown(f"{i}. [{title}]({url})")


def render_passages(result) -> None:
    label = f"Passages retrieved ({len(result.chunks)})"
    with st.expander(label):
        for chunk in result.chunks:
            cited = chunk.rank in result.cited_ranks or not result.cited_ranks
            mark = "cited" if cited else "retrieved, not cited"
            st.markdown(
                f"**[{chunk.rank}] {chunk.title}** — similarity "
                f"`{chunk.similarity:.3f}` · _{mark}_"
            )
            if chunk.section:
                st.caption(chunk.section)
            st.text(chunk.text)
            st.divider()


st.title("💖 The Curly Girl Unofficial Guide")
st.caption(
    "Natural and curly hair care, answered only from a fixed set of community "
    "sources — Reddit threads, forums, and hair-care blogs."
)

with st.sidebar:
    st.header("Settings")
    top_k = st.slider(
        "Passages retrieved (top-k)", min_value=1, max_value=10, value=TOP_K
    )
    min_similarity = st.slider(
        "Relevance threshold",
        min_value=0.0,
        max_value=0.9,
        value=MIN_SIMILARITY,
        step=0.05,
        help="Passages scoring below this are dropped. If none survive, the "
        "guide refuses instead of guessing.",
    )

    st.divider()
    st.caption("**Pipeline**")
    st.caption(f"Embedding · `{EMBEDDING_MODEL}`")
    st.caption("Vector store · `ChromaDB` (cosine)")
    st.caption(f"Generation · `{MODEL}`")

    try:
        st.caption(f"Indexed chunks · `{load_collection().count()}`")
    except Exception:
        st.error("No index found. Run `python ingest.py` then `python retrieval.py --build`.")
        st.stop()

st.markdown("**Try one of the test questions**")
columns = st.columns(len(EVAL_QUESTIONS))
picked = None
for column, question, label in zip(columns, EVAL_QUESTIONS, TOPIC_LABELS):
    # The button shows the topic; the full question goes in the box on click
    # and is available on hover.
    if column.button(label, help=question, use_container_width=True):
        picked = question

question = st.text_input(
    "Your question",
    value=picked or "",
    placeholder="e.g. How do I keep my twist-out from frizzing in humidity?",
)

if st.button("Ask", type="primary") or picked:
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Retrieving passages and generating a grounded answer..."):
            try:
                result = answer_question(
                    question,
                    top_k=top_k,
                    min_similarity=min_similarity,
                    collection=load_collection(),
                )
            except Exception as error:
                st.error(f"Something went wrong: {error}")
                st.stop()

        st.markdown("### Answer")
        st.markdown(result.answer)

        if result.refused:
            st.info(
                "Nothing in the guide scored above the relevance threshold, so "
                "no answer was generated."
            )
        else:
            st.divider()
            render_sources(result)
            render_passages(result)
