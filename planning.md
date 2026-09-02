# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels?

The domain I chose is how to style and maintain naturally curly hair, specifically based on different hairstyles and hair types. This knowledge is valuable because many people beginning their natural hair care journey do not know where to start or who to trust due to the amount of conflicting information available online. Advice about styling techniques, products, and hair types is often spread across social media, blogs, forums, and personal experiences rather than being available through one reliable source. This project will bring that information together in one central place, making it easier for people interested in natural hair care to find practical and relevant guidance.

 --> 



---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Blog | Gives a crash course on hair density, including what it is, how to determine hair density, and why it can matter for hair care. |https://curlsmith.com/blogs/curl-academy/hair-density-meaning-test-care |
| 2 | Subreddit| Discusses products that may help with fine, high-density curly hair on wash day based on the user's personal experience. |  https://www.reddit.com/r/curlyhair/comments/1loteew/how_do_i_keep_my_fine_dense_high_porosity_curls/  |
| 3 | Blog | Gives an overview of length retention and provides specific routines and tips for those interested in growing their hair and maintaining its health. | https://www.blackcurlmagic.com/blog/the-truth-about-length-retention-for-natural-hair |
| 4 |Subreddit | A Reddit user who works out regularly asks how others maintain natural hair between washes and preserve hairstyles after exercising. Community members share different approaches based on their workout frequency, hairstyles, and personal preferences.|https://www.reddit.com/r/Naturalhair/comments/1u602mn/for_those_of_you_thay_are_active_with_natural_hair/? |
| 5 | Forum | Discusses curl types and provides product recommendations for styling both looser and tighter curl patterns. https://forum.looksmaxxing.com/threads/hair-care-pt-1-finding-your-curl-type-and-products-to-use-simple-version.160343/ |
| 6 | Subreddit | A community discussion about heat-damaged hair that includes users' experiences and methods for restarting or adjusting their natural-hair routines. |  https://www.reddit.com/r/Naturalhair/comments/1p7f1l6/damage_advice/ |
| 7 | Blog | Discusses protective hairstyles for different curl patterns and how they may help reduce manipulation. | https://www.crystalaguhmd.com/post/choosing-the-best-summer-protective-style-for-your-curl-pattern|
| 8 | Subreddit | Community members share strategies for preserving natural hairstyles and reducing frizz in humid conditions.| https://www.reddit.com/r/Naturalhair/comments/1ki3a2z/how_ldo_yall_fight_humidity/ |
| 9 | Subreddit| A community discussion focused on 4C hair, including styling techniques, maintenance practices, and product. | https://www.reddit.com/r/Naturalhair/comments/1fgbtrv/styling_tips_4c_hair_i_hate_it/  |
| 10 | Subreddit | Discusses low-porosity hair through a user's personal hair-care journey, including routine and product considerations. | https://www.reddit.com/r/curlyhair/comments/bce9uh/my_low_porosity_hair_journey_porosity_matters/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
