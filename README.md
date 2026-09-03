# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Demo Video Link
https://canva.link/brrtrn9uf7jbvcg

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

 - The domain I chose is how to style and maintain naturally curly hair, specifically based on different hairstyles and hair types. This knowledge is valuable because many people beginning their natural hair care journey do not know where to start or who to trust due to the amount of conflicting information available online. Advice about styling techniques, products, and hair types is often spread across social media, blogs, forums, and personal experiences rather than being available through one reliable source. This project will bring that information together in one central place, making it easier for people interested in natural hair care to find practical and relevant guidance.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
- 100 tokens

**Overlap:**
- 20 tokens 

**Why these choices fit your documents:**
- I initially planned to use 500 token chunks with a 75 token overlap. During implementation, the resulting chunks were too large and produced only 14 chunks across the 10 documents. Larger chunks also risk including unrelated information, which could make retrieval less precise for specific user questions. I therefore changed the strategy to 100 token chunks with a 20 token overlap. The smaller chunks should allow the retrieval system to identify more specific pieces of information while the overlap helps preserve context across chunk boundaries.

**Final chunk count:** 
- 81 chunks

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

| # | Source document | Chunk text |
|---|----------------|------------|
| 1 | fine_hi_po.txt| Fine, high-porosity curly hair. Cleansing conditioner may be too heavy for fine hair. Consider using a clarifying shampoo or low-poo shampoo instead. Less product may be more effective for fine hair. High-porosity hair can benefit from heavier creams and oils, but using too many moisturizing products at once may be unnecessary. When hair is very dry, use one moisturizing hair mask rather than layering multiple heavy products. |
| 2 | 4c_styling_maintenance.txt | Work from the ends toward the roots to help minimize unnecessary pulling and breakage. Sectioning the hair before and during detangling can make the process easier. Leave-in conditioner can be added after washing and conditioning when additional moisture is needed. Moisturizing products such as creams, butters, and oils can be used depending on the hair's needs. Products mentioned as examples include Camille Rose Curl Maker, Camille Rose Honey, and As I Am Curl products. |
| 3 | hair_density.txt | At home, density can be estimated by measuring the circumference of a dry ponytail. Suggested ponytail measurements: High density: greater than 4 inches; Medium density: 2–3 inches; Low density: less than 2 inches. For hair that is too short to measure in a ponytail, scalp visibility and the width of the part can provide an indication of density. Hair density can influence how much volume or fullness a person naturally has. |
| 4 | gym_maintenance.txt | Tie the hair down during workouts. Allow the hair to dry before removing the scarf or wrap. Use refresher products, mousse, or edge control to manage frizz afterward. |
| 5 |gym_maintenance.txt| One commenter emphasized that natural hair does not need to look perfectly styled at all times and that maintaining physical health through exercise can be more important than keeping a hairstyle perfectly intact. The discussion demonstrates several different approaches, including exercising normally without worrying about temporary frizz or shrinkage, maintaining the hairstyle for several weeks, and using mousse or other products when the style begins to look less polished. |

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** 
- I used the all-MiniLM-L6-v2 via sentence-transformers embedding model because it was free and readily available for use. 

**Production tradeoff reflection:**
- If this system were deployed for real users, I would consider a more advanced embedding model if it provided better retrieval accuracy for domain-specific hair-care terminology. I would also consider context length, multilingual support, and latency. A more accurate model may improve retrieval quality, but it could also require more computational resources and increase response time.
---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:** -->  My natural hair has heat damage. What approaches should be used to adjust my rotuine and care for my hair afterward?

Top returned chunks:
- [1] heat_damage_tips::7   similarity 0.628
      doc     : HEAT DAMAGE AND CURL DAMAGE — COMMUNITY ADVICE
      section : TREATMENTS DISCUSSED BY THE COMMUNITY | PROTEIN TREATMENTS
      source  : https://www.reddit.com/r/Naturalhair/comments/1p7f1l6/damage_advice/
      Bond-building products mentioned by commenters included Olaplex, Redken,
      L'Oréal, and Curlsmith products. These recommendations are based on
      individual community experiences and should not be treated as guaranteed
      solutions for reversing heat damage. PROTEIN TREATMENTS Protein
      treatments were recommended by some community members to improve the
      strength and elasticity of damaged hair. Protein treatments should not
      necessarily be used excessively. Too much protein can contribute to
      stiffness, dryness, or breakage for some hair.

  [2] heat_damage_tips::9   similarity 0.613
      doc     : HEAT DAMAGE AND CURL DAMAGE — COMMUNITY ADVICE
      section : HEAT-PROTECTION PRACTICES
      source  : https://www.reddit.com/r/Naturalhair/comments/1p7f1l6/damage_advice/
      Apply heat protectant evenly in sections rather than spraying it over
      the entire head at once. Avoid flat-ironing hair at excessively high
      temperatures. Reduce the frequency of heat styling. Avoid additional
      heat while recovering from existing heat damage. Allow hair to dry
      partially before blow-drying rather than applying high heat to soaking-
      wet hair. Use lower or moderate heat settings when possible. Some
      commenters recommended using multiple heat-protection products and
      products rated for temperatures up to 450°F.

  [3] heat_damage_tips::6   similarity 0.585
      doc     : HEAT DAMAGE AND CURL DAMAGE — COMMUNITY ADVICE
      section : STYLING WHILE GROWING OUT DAMAGE | TREATMENTS DISCUSSED BY THE COMMUNITY
      source  : https://www.reddit.com/r/Naturalhair/comments/1p7f1l6/damage_advice/
      Wigs with lower-tension construction Low-tension styles may be
      preferable when the hair is already damaged or fragile. TREATMENTS
      DISCUSSED BY THE COMMUNITY Community members suggested several types of
      treatments for damaged hair: Bond-building treatments Protein treatments
      Deep conditioning Hair masks Steam or heat-assisted deep conditioning
      Bond-building products mentioned by commenters included Olaplex, Redken,
      L'Oréal, and Curlsmith products.

Relevance explanation: 
- The retrieved chunks are highly relevant as all three come from the heat-damage discussion and directly address ways to care for hair after heat damage. Chunk 1 discusses bond-building and protein treatments for damaged hair, while also noting that these are based on individual community experiences. Chunk 2 focuses on reducing heat exposure, using heat protectant, and adjusting heat-styling practices. Chunk 3 provides additional approaches such as low-tension styles, deep conditioning, hair masks, and other treatments discussed by the community. Together, these chunks provide several approaches for adjusting a routine after experiencing heat damage.

---

**Query 2:** --> What practices help me retain length while maintaining healthy natural hair? 

Top returned chunks:
- [1] gym_maintenance::9   similarity 0.624
      doc     : NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE
      section : MAINTAINING HAIR BETWEEN WASHES | DIFFERENT APPROACHES TO WORKOUT HAIR | 1. LOW-MAINTENANCE APPROACH
      source  : https://www.reddit.com/r/Naturalhair/comments/1u602mn/for_those_of_you_thay_are_active_with_natural_hair/?
      One commenter emphasized that natural hair does not need to look
      perfectly styled at all times and that maintaining physical health
      through exercise can be more important than keeping a hairstyle
      perfectly intact. DIFFERENT APPROACHES TO WORKOUT HAIR The discussion
      demonstrates several different approaches: 1. LOW-MAINTENANCE APPROACH *
      Exercise normally without worrying about temporary frizz or shrinkage. *
      Maintain the hairstyle for several weeks. * Use mousse or other products
      when the style begins to look less polished.

  [2] 4c_styling_maintenance::8   similarity 0.617
      doc     : 4C NATURAL HAIR — PRODUCTS, STYLING, AND MAINTENANCE
      section : PROTECTIVE & LOW-MANIPULATION STYLING | HEAT & LENGTH RETENTION
      source  : https://www.reddit.com/r/Naturalhair/comments/1fgbtrv/styling_tips_4c_hair_i_hate_it/
      Protective styles can reduce the need for frequent manipulation. Styles
      should not create excessive tension on the scalp. Tight braids,
      cornrows, ponytails, and extensions can contribute to hair breakage and
      traction-related hair loss. If experiencing thinning or bald areas,
      avoid tight hairstyles and styles involving added synthetic hair. HEAT &
      LENGTH RETENTION Blow-drying does not necessarily require completely
      straightening the hair; hair can be mostly dried while remaining in a
      natural state.

  [3] gym_maintenance::8   similarity 0.609
      doc     : NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE
      section : MAINTAINING HAIR BETWEEN WASHES | DIFFERENT APPROACHES TO WORKOUT HAIR
      source  : https://www.reddit.com/r/Naturalhair/comments/1u602mn/for_those_of_you_thay_are_active_with_natural_hair/?
      * Retwist or rebraid sections when necessary. * Use low-manipulation
      styles that can last through multiple workouts. * Accept some frizz and
      shrinkage rather than repeatedly restyling the hair. One commenter
      emphasized that natural hair does not need to look perfectly styled at
      all times and that maintaining physical health through exercise can be
      more important than keeping a hairstyle perfectly intact. DIFFERENT
      APPROACHES TO WORKOUT HAIR The discussion demonstrates several different
      approaches:

Relevance explanation:

---

**Query 3:** --> How do hair care reccomendations differ between low-porosity and high-porosity hair, especially when it comes to products and styling? 

Top returned chunks:
- [1] lo_po_reddit::5   similarity 0.774
      doc     : LOW-POROSITY CURLY HAIR — ROUTINE AND PRODUCT EXPERIENCE
      section : GENERAL APPROACH
      source  : https://www.reddit.com/r/curlyhair/comments/bce9uh/my_low_porosity_hair_journey_porosity_matters/
      Hair-care routines should be adjusted based on individual hair
      characteristics and how the hair responds to specific products and
      ingredients. Low-porosity hair may benefit from a simpler routine with
      lightweight products, controlled product usage, and regular cleansing.

  [2] fine_hi_po::4   similarity 0.724
      doc     : REDDIT USER — FINE, HIGH-POROSITY CURLY HAIR ROUTINE
      section : GENERAL APPROACH
      source  : https://www.reddit.com/r/curlyhair/comments/1loteew/how_do_i_keep_my_fine_dense_high_porosity_curls/
      Keep the routine simple and consistent. Be patient when determining what
      works for fine, high-porosity hair. The user's overall approach is to
      avoid product buildup while still providing enough moisture for high-
      porosity hair.

  [3] lo_po_reddit::3   similarity 0.693
      doc     : LOW-POROSITY CURLY HAIR — ROUTINE AND PRODUCT EXPERIENCE
      section : STYLING ROUTINE | OBSERVED BENEFITS
      source  : https://www.reddit.com/r/curlyhair/comments/bce9uh/my_low_porosity_hair_journey_porosity_matters/
      Limit the number of products layered onto the hair. Pay attention to the
      amount of product being used rather than automatically applying multiple
      products. Lightweight oils and products may be more appropriate for low-
      porosity hair. Consider ingredients such as humectants when developing a
      low-porosity routine. OBSERVED BENEFITS Adjusting the routine to account
      for low porosity and protein sensitivity may result in: Softer-feeling
      hair Increased volume Reduced frizz Less product buildup

Relevance explanation:
- The retrieved chunks are relevant because the query asks for a comparison between low-porosity and high-porosity hair, and the results include information about both. Chunk 1 and Chunk 3 describe recommendations for low-porosity hair, including using lightweight products, limiting product buildup, and avoiding excessive layering. Chunk 2 provides recommendations for fine, high-porosity hair, including maintaining moisture while avoiding too much product buildup. Together, the retrieved chunks allow the system to compare how product and routine recommendations may differ based on porosity.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** 
The system prompt instructs the model to answer the user's question using only the retrieved context provided to it. If the retrieved context does not contain enough information to answer the question, the model is instructed to say that the guide does not contain the information rather than relying on outside knowledge. The prompt also instructs the model to cite the retrieved sources when providing information.

**How source attribution is surfaced in the response:**
The interface displays source citations alongside the generated answer using numbered references such as [1] and [2]. Below the answer, the system displays the source names, retrieved passages, similarity scores, and links to the original sources, allowing the user to see where the answer came from and inspect the supporting information.
---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query: I work out several times a week and don't want to wash my natural hair after every workout. How can I maintain my hairstyle between workouts?

Response: Answer
Use low‑maintenance styles that tolerate sweat, such as braids, twists, mini‑braids, or a low‑manipulation ponytail/bun. These can be left in for several weeks and refreshed when needed [3][4].
When the style starts to look frizzy, apply a hair refresher spray or a bit of mousse to revive the look without a full wash [1][2].
Dry shampoo is another option some commenters use after a workout to absorb sweat and reduce frizz [1].
If the style becomes difficult to manage, re‑braid or retwist the hair, or pull the existing twists into a new ponytail or bun [3][4].
These approaches let you exercise several times a week while keeping your natural hair looking presentable between washes.

Source attribution: Sources

NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE
Passages retrieved (5)
[1] NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE — similarity 0.720 · cited

MANAGING FRIZZ AFTER WORKOUTS | WASHING AND CLEANSING

* Use a hair refresher spray after exercising.
* Some commenters recommended dry shampoo as another post-workout option.

The effectiveness of these methods may vary depending on the individual's hair type, hairstyle, and amount of sweating.

WASHING AND CLEANSING

The community has different opinions about how frequently natural hair should be washed when exercising.

* Some people wash weekly or every two weeks.
* Some wash more frequently when they sweat heavily.

---

**Grounded response 2**

Query: How do I keep my twist-out from frizzing in humidity?

Response: Answer
Use a strong‑hold gel or styling product designed for humidity protection to lock the twist‑out in place【1†L2-L4】【3†L2-L4】.
Consider adding an anti‑humidity spray or serum on top of the gel for extra barrier against moisture【3†L2-L4】.
Curl creams or custards that promise stronger hold can also be layered under the gel to boost definition【3†L2-L4】.
Some commenters suggest that completely preventing frizz in very humid conditions may be unrealistic, so embracing a bit of natural shrinkage and frizz while focusing on hold is another approach【1†L1-L3】【5†L1-L4】.

Source attribution: Sources

HUMIDITY, FRIZZ, AND SHRINKAGE — COMMUNITY ADVICE
NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE
Passages retrieved (5)
[1] HUMIDITY, FRIZZ, AND SHRINKAGE — COMMUNITY ADVICE — similarity 0.659 · cited

HOW HUMIDITY AFFECTS NATURAL HAIR | STRONG-HOLD STYLING PRODUCTS

Several commenters suggest that completely preventing frizz or shrinkage may not be realistic in highly humid environments.
Some commenters recommend accepting or embracing shrinkage and frizz rather than trying to completely prevent them.

---

**Out-of-scope query**

Query: Where can I watch the Odessey?

System response (refusal): I don't have anything in the guide that answers that. This guide only covers natural and curly hair care — styling, washing, porosity, protective styles, heat damage, humidity, and length retention — drawn from a fixed set of blogs and Reddit threads. 

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:** 
- There are two fields. The first field is where you can submit a question that's "suggested" by the model ( which uses the questions I put in the planning.md file). The other input field is a text box where the user can write any query they may have.

**Output format:**
- After clicking the "ASK" button, there is a section labeled "Answer" that will say it's generating an answer. After the answer is generated, it will give a list of relevant sources/passagfes, with citations. If you scroll to the bottom of the page, then you will see the actual sources and links that the model pulled from, so users can explore the link itself if they want to. "Below that, there is a section where the bot shows exactly which processed passages were used to generate the answer, along with a relevance score for each retrieved chunk."

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** What styling techniques, maintenance practices, and product recommendations are discussed for 4C natural hair?

> **System:** Answer
Styling techniques

Low‑maintenance approach: keep the same style for several weeks and accept temporary frizz or shrinkage, using mousse or similar products when the look becomes less polished [1][5].
Protective approach: wear braids or twists while exercising, securing the hair with a scarf, sweatband, or satin‑lined cap; re‑braid or retwist as needed [1][2].
Low‑manipulation styles that can survive multiple workouts, with occasional retwisting or rebonding of sections [3].
Maintenance practices

Retwist or rebraid sections when necessary [3].
Wash the hair after frequent workouts (frequent‑wash approach) or follow a schedule ranging from weekly to every two weeks depending on the style [1][4].
Deep‑condition for added moisture, especially for thick 4C hair that benefits from moisture‑retention routines [4].
Avoid keeping protective styles installed for excessively long periods to reduce breakage [2].
Product recommendations

Use mousse (or comparable styling products) when the style begins to look less polished [1][5].
Shampoo and conditioner on wash days, with deep‑conditioning treatments as part of the routine [4].
Sources

NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE
PROTECTIVE STYLES — CURL PATTERN, DENSITY, AND BREAKAGE
4C NATURAL HAIR — PRODUCTS, STYLING, AND MAINTENANCE
Passages retrieved (5) 
[1] NATURAL HAIR AND WORKOUT MAINTENANCE — COMMUNITY ADVICE — similarity 0.642 · cited

LOW-MAINTENANCE APPROACH | 2. PROTECTIVE APPROACH | 3. FREQUENT-WASH APPROACH
* Maintain the hairstyle for several weeks.
* Use mousse or other products when the style begins to look less polished.

2. PROTECTIVE APPROACH

* Exercise while wearing braids or twists.
* Secure the hair with a scarf, sweatband, or satin-lined cap.
* Wash the hair while it remains in the style.
* Rebraid or retwist when necessary.

3. FREQUENT-WASH APPROACH

* Wash the hair after frequent or daily workouts.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What styling techniques, maintenance practices, and product recommendations are discussed for 4C natural hair? | The system should retrieve the Reddit discussion about 4c hair and identify the products and techniques discussed by the user/community. The answer should make clear that these are personal/community recommendations, rather than universally proven rules.| Provides styling techniques, maintenance practices, and product recommendations, but pulls mainly from the Gym maintenance protective style articles. Only pulls some info from the 4c subreddit. |Relevant | Partially accurate |

| 2 | What practices can help me retain length while maintaining healthy natural hair? | The system should retreieve information from the Black Curl Magic blog. It should discuss practices such as protective styling, reducing manipulation,and maintaining healthy hair practices. | Gives information about low manipulation/protective styles, maintaining moisture, and trimming ends, but pulls from the Gym maintenance and 4c maintenance. It does pull a good amount from the hair retention article though. | Relevant | Partially accurate |

| 3 | I work out several times a week and don't want to wash my natural hair after every workout. How can I maintain my hairstyle between workouts?| The system should retrieve from the workout Reddit discussion and explain strategies users shared for maintaining hair between workouts. It should discuss how to protect the hair during exercise, managing sweat, and refreshing the hairstyle. | Pulls only from gym maintenance about how to keep a hairstyle for longer as well as how to adjust your hair care and washing routine to continue exercising. | Relevant |Accurate |
| 4 | My natural hair has heat damage. What approaches should be used to adjust my routine and care for my hair afterward?| The system should retrieve from the heat damage Reddit discussion and summarize the approaches and experiences shared by users. It should avoid using the indivudal experiences as guaranteed treatments.| Pulls majority information from the Heat and Curl Damage subreddit, with it being the number 1 source. Gives tips like adding heat protection into your routine, using restorative products, and trimming ends.| Relevant | Accurate |
| 5 | How do hair-care recommendations differ between low-porosity and high-porosity hair, especially when it comes to products and styling?  The system should retrieve information from both the low-porosity and high-porosity sources and compare the product and styling recommendations discussed in each. The response should explain differences in how the sources describe caring for low- and high-porosity hair and should distinguish personal experiences from universally established facts.| The system has two chunks talking about low porosity and high porosity hair and only sources the subreddits that are about high and low porosity hair. Beautifully accurate.| Relevant | Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**  
What styling techniques, maintenance practices, and product recommendations are discussed for 4C natural hair? 

**What the system returned:**
The system returned some relevant information about natural hair styling and maintenance, but the most directly relevant 4C-specific information was not included in the initial top 3 retrieved chunks. The correct 4C source ranked fourth in similarity, while more general natural-hair content ranked higher.

**Root cause (tied to a specific pipeline stage):**
The issue occurred during the retrieval stage. The embedding-based similarity search ranked some more general hair-maintenance chunks above the 4C-specific chunk because they contained overlapping terms related to styling, maintenance, and products. As a result, the most specific source was initially excluded when using a top-k value of 3.

**What you would change to fix it:**
I increased the retrieval top-k from 3 to 5 so that relevant chunks ranked slightly lower are still included in the retrieved context. I could also improve the document/chunk metadata or retrieval strategy to give the system more information about the specific topic of each chunk. I would not rely primarily on changing the system prompt because this issue occurs before generation, during retrieval.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec gave me a clear idea of how I was going to implement each stage, regardless if I knew how to code it or not. If soemthing went wrong, I could go back to my specs and see if I implemented soemthing wrong in the initial planning stage or an issue from the code. For example, when my initial chunking strategy produced chunks that were too large, I was able to recognize that the issue was with my planned chunk size rather than the overall pipeline. Similarly, testing the Groq and OpenAI implementations helped me identify a discrepancy in how the two systems were handling the pipeline.

**One way your implementation diverged from the spec, and why:**
I had to diverge a lot when I was initally planning the chunk size, overlap, and top-k size. I had to constantly play with the settings so that my chunk sizes were not too large or small, but still fit within the limits of the vector embedding. I changed the chunking strategy to 100-token chunks with a 20-token overlap and increased top-k to 5 based on these results. This iterative process made it easier to debug the system and identify exactly where revisions were needed.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* Use the planning.md and pipeline diagram to generate the generation and interface code. The prompt should include: the grounding requirement (answers from retrieved context only, with source attribution), the output format (answer + source list), and the streamlit skeleton structure if you're using it. Wire it all together.

- *What it produced:* The AI produced the Streamlit interface and connected it to my RAG pipeline. It also helped ensure that the generation portion worked with the model I was using, since I used a different model from the one in the original repository.

- *What I changed or overrode:* I customized the Streamlit UI to better match the appearance and style I envisioned. I also tested the application myself rather than assuming the generated code was working correctly.

**Instance 2**

- *What I gave the AI:* I gave the AI my planned chunking strategy from planning.md and asked it to implement the document chunking portion of the pipeline using a target chunk size and overlap.

- *What it produced:* The AI initially implemented a chunking approach based on my original plan of 500-token chunks with a 75-token overlap. When I tested it, the resulting chunks were too large and the pipeline produced only 14 chunks across my 10 documents.

- *What I changed or overrode:* I changed the chunking strategy to 100-token chunks with a 20-token overlap after testing the initial implementation. I also directed the AI to make the chunking more content-aware so that chunks would preferably end at sentence or paragraph boundaries instead of cutting off in the middle of a sentence. I then inspected random chunks myself to make sure the results were readable and useful for retrieval.
