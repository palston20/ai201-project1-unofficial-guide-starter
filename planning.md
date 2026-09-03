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
     State your chunk size (in tokens or characters), overlap size, and explain why those numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ.
      -->

**Chunk size:** --> 250 tokens

**Overlap:** --> 40 tokens

**Reasoning:** --> I initially planned to use 500 token chunks with a 75 token overlap. During implementation, the resulting chunks were too large and produced only 14 chunks across the 10 documents. Larger chunks also risk including unrelated information, which could make retrieval less precise for specific user questions. I therefore changed the strategy to 100 token chunks with a 20 token overlap. The smaller chunks should allow the retrieval system to identify more specific pieces of information while the overlap helps preserve context across chunk boundaries.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)? 
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs would you weigh in choosing a different embedding model — context length, multilingual support, accuracy on domain-specific text, latency? 

-->
**Embedding model:**
--> all-MiniLM-L6-v2 via sentence-transformers
**Top-k:**
--> 3 chunks 
**Production tradeoff reflection:**
--> If this system were deployed for real users, I would consider a more advanced embedding model if it provided better retrieval accuracy for domain-specific hair-care terminology. I would also consider context length, multilingual support, and latency. A more accurate model may improve retrieval quality, but it could also require more computational resources and increase response time.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What styling techniques, maintenance practices, and product recommendations are discussed for 4C natural hair? | The system should retrieve the Reddit discussion about 4c hair and identify the products and techniques discussed by the user/community. The answer should make clear that these are personal/community recommendations, rather than universally proven rules. |
| 2 | What practices can help me retain length while maintaining healthy natural hair? | The system should retreieve information from the Black Curl Magic blog. It should discuss practices such as protective styling, reducing manipulation,and maintaining healthy hair practices.|
| 3 | I work out several times a week and don't want to wash my natural hair after every workout. How can I maintain my hairstyle between workouts?| The system should retrieve from the workout Reddit discussion and explain strategies users shared for maintaining hair between workouts. It should discuss how to protect the hair during exercise, managing sweat, and refreshing the hairstyle. |
| 4 | My natural hair has heat damage. What approaches should be used to adjust my routine and care for my hair afterward? | The system shoudl retrieve from the heat damage Reddit discussion and summarize the approaches and experiences shared by users. It should avoid using the indivudal experiences as guaranteed treatments. |
| 5 | How do hair-care recommendations differ between low-porosity and high-porosity hair, especially when it comes to products and styling?| TThe system should retrieve information from both the low-porosity and high-porosity sources and compare the product and styling recommendations discussed in each. The response should explain differences in how the sources describe caring for low- and high-porosity hair and should distinguish personal experiences from universally established facts.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.The first risk is that the system may retrieve chunks that have similar keywords, but are not actually relevant to the user's question. This could result in irrelevant responses. 

2.The second risk is that the chunking may separate relevant information across different chunks. For examples, a hair type might be explained in one chunk while its corresponding styling reccomendation may appear in another. If only one chunk is retrieved, then the system will lack enough context to provide a decent answer. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

┌──────────────────────────────┐
│ 1. Document Ingestion        │
│ Python + Processed TXT Files │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 2. Chunking                  │
│ Fixed-Size + Overlap         │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 3. Embedding + Vector Store  │
│ sentence-transformers        │
│ (all-MiniLM-L6-v2) + ChromaDB│
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 4. Retrieval                 │
│ ChromaDB Similarity Search   │
│ Top-k = 3                    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ 5. Generation                │
│ gpt-oss-120b + Context       │
└──────────────────────────────┘

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)


     - What you expect it to produce?
     

     - How you'll verify the output matches your spec?
     


     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
--> I will provide Claude with my documents and chunking strategiy sections and ask it to implement the document ingestion adn chunking pipeline. The code should read my processed .txt files and divide them into 500 token chunks with a 75 token overlap. I will inspect the generated chunks to verify the text is organzed correctly and that important information is not unnecessarily separated.

**Milestone 4 — Embedding and retrieval:**
--> Claude will receieve my retrieval approach and archtiecture sections and ask it to implement the embedding and retrieval pipeline. It should use all-MiniLM-L6-v2 through sentence-transformers to create embeddings and ChromaDB to store them. The retrieval system should return the top 3 most relevant chunks for each user query. I will verify the retrieval results using my five evaluation questions and check whether the retrieved chunks are relevant to each question.

**Milestone 5 — Generation and interface:**
--> I will provide Claude with my evaluation plan and ask it to implement the generation stage and Streamlit interface. The system should pass the retrieved chunks as context to gpt-oss-120b so that it generates answers based on the provided sources. I will test the interface using my five evaluation questions and compare the generated answers with the source documents to check for accuracy and unsupported information.
