# ChatGPT Sentence Constructor Activity

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Summary Table: 4o vs. o1 Model Performance](#summary-table-4o-vs-o1-model-performance)
- [Introduction](#introduction)
  - [Key Questions Explored](#key-questions-explored)
  - [Summary of Findings](#summary-of-findings)
- [Method](#method)
  - [Models Tested](#models-tested)
  - [Experiment Setup](#experiment-setup)
  - [Why Use Temporary Chats?](#why-use-temporary-chats)
  - [Testing Approach](#testing-approach)
- [Prompt](#prompt)
  - [Why This Prompt?](#why-this-prompt)
    - [Key Design Choices & Intentions](#key-design-choices--intentions)
- [Results](#results)
  - [Portuguese (Beginner Level)](#portuguese-beginner-level)
    - [Test Sentence (PT)](#test-sentence-pt)
    - [4o Model Response (PT)](#4o-model-response-pt)
    - [o1 Model Response (PT)](#o1-model-response-pt)
    - [Portuguese Prompt – 4o vs. o1 Model Responses](#portuguese-prompt--4o-vs-o1-model-responses)
    - [Conclusion (PT)](#conclusion-pt)
  - [French (Intermediate Level)](#french-intermediate-level)
    - [Test Sentence (FR)](#test-sentence-fr)
    - [4o Model Response (FR)](#4o-model-response-fr)
    - [o1 Model Response (FR)](#o1-model-response-fr)
    - [French Prompt – 4o vs. o1 Model Responses](#french-prompt--4o-vs-o1-model-responses)
    - [Conclusion (FR)](#conclusion-fr)
  - [English (Advanced Level: Adjective Order Test)](#english-advanced-level-adjective-order-test)
    - [Test Sentence (EN)](#test-sentence-en)
    - [4o Model Response (EN)](#4o-model-response-en)
    - [o1 Model Response (EN)](#o1-model-response-en)
    - [English Prompt – 4o vs. o1 Model Responses](#english-prompt--4o-vs-o1-model-responses)
    - [Conclusion (EN)](#conclusion-en)
  - [Spanish (Expert Level: Medical Terminology)](#spanish-expert-level-medical-terminology)
    - [Test Sentence (ES)](#test-sentence-es)
    - [4o Model Response (ES)](#4o-model-response-es)
    - [o1 Model Response (ES)](#o1-model-response-es)
    - [Spanish Prompt – 4o vs. o1 Model Responses](#spanish-prompt--4o-vs-o1-model-responses)
    - [Conclusion (ES)](#conclusion-es)
  - [Overall Observations](#overall-observations)
- [Conclusion & Next Steps](#conclusion--next-steps)
  - [Key Takeaways](#key-takeaways)
  - [Next Steps & Potential Improvements](#next-steps--potential-improvements)
  - [Final Thoughts](#final-thoughts)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Summary Table: 4o vs. o1 Model Performance

| Language          | Sentence Complexity         | 4o Model Response | o1 Model Response | Key Observations |
|------------------|--------------------------|------------------|------------------|------------------|
| **Portuguese** (Beginner) | Simple sentence with minor grammar errors | Inconsistent feedback; sometimes gave full answer instead of hints | More structured feedback; responded in Portuguese, assuming user proficiency | o1 provided a more pedagogically valuable response but was slower |
| **French** (Intermediate) | Sentence with multiple grammar and vocabulary mistakes | Friendly and engaging; used emojis | Precise and professional; did not use emojis | o1 was more direct, while 4o was more interactive and supportive |
| **English** (Advanced) | Complex adjective ordering test | Missed key learning point initially; focused on sentence length instead | Provided better hints but still required a follow-up prompt | o1 had a more structured approach but needed prompting |
| **Spanish** (Expert) | Advanced sentence with specialized vocabulary | Identified minor terminology improvement | Identified same issue; slightly warmer tone | Both models performed well, but o1 maintained a more professional tone |

## Introduction

This document presents the results of an experiment comparing OpenAI’s **4o** and **o1** models in a **sentence construction activity** designed for language learners. The goal was to evaluate how well each model provides **pedagogically valuable feedback** when correcting or improving sentences written in different languages.

The models were tested using **ChatGPT’s temporary chat feature** to prevent memory retention and ensure fresh responses for each attempt. Sentences of varying complexity were tested in **Portuguese (beginner), French (intermediate), English (advanced), and Spanish (expert)** to analyze how each model handles different proficiency levels.

### Key Questions Explored

1. **Consistency** – Does the model respond reliably to similar prompts?
2. **Pedagogical Value** – Does the feedback promote active learning instead of just providing corrections?
3. **Language Adaptability** – Does the model correctly assess the user’s language level and respond appropriately?
4. **Response Tone & Style** – Does the model maintain a professional, friendly, and engaging tone?
5. **Speed & Efficiency** – How long does the model take to generate responses?

### Summary of Findings

- **o1 model** generally provided more **structured, pedagogically valuable, and professional** feedback.
- **4o model** was more **playful and engaging**, but sometimes inconsistent.
- Response times varied significantly, with **o1 taking longer** in all cases.
- **Both models performed well at higher proficiency levels**, but the **4o model struggled with consistency at lower levels**.

The following sections present a detailed breakdown of the methodology, prompts used, and individual language-specific results.

## Method

### Models Tested

- **4o Model** (OpenAI’s default GPT-4o)
- **o1 Model** (More recent OpenAI model)

### Experiment Setup

- **Platform:** ChatGPT with a **Plus subscription** ($20/month).
- **Testing Environment:** **Temporary chat** mode to prevent memory retention.
- **Interaction Style:** The models were addressed **as a language tutor** to simulate a real-world tutoring scenario.
- **Evaluation Focus:** The models were assessed based on **consistency, pedagogical value, adaptability, tone, and efficiency**.

### Why Use Temporary Chats?

ChatGPT's **temporary chat mode** ensures that each interaction is **stateless**, meaning:

✔️ The model does not retain context from previous messages.  
✔️ Responses are **not influenced by prior interactions**, ensuring fairness in testing.  
⚠️ **Drawback:** Once the chat is closed, the conversation history is lost, making post-analysis more challenging.

### Testing Approach

1. **A sentence was submitted in a target language** (Portuguese, French, English, or Spanish).
2. The model was **prompted to provide feedback** without revealing the correct answer.
3. **Corrections and improvements were analyzed** based on clarity, effectiveness, and adherence to the prompt.
4. If the model’s response was **inconsistent or incomplete**, a follow-up prompt was given.
5. The **response time and style** were noted.

The next section outlines the **exact prompt** used for each test.

## Prompt

To evaluate how well each model performs as a **language tutor**, we used a structured prompt designed to encourage **progressive learning** rather than just providing corrections. This ensures that the models offer **constructive feedback** while allowing the learner to improve their sentence naturally.

```text
You are my language tutor. I will write a sentence in [target language], and your role is to help me improve without giving me the answer directly.

If my sentence is correct, confirm that it is correct and suggest a small improvement if possible.

If my sentence has mistakes, point them out by explaining what kind of error I made (e.g., grammar, word choice, syntax), and give hints or examples to help me correct it myself without revealing the full correct sentence. Encourage me to try again, and only reveal the correct version if I struggle after a few attempts.

Keep your feedback friendly, supportive, and constructive to make learning engaging.
```

### Why This Prompt?

This prompt was carefully designed to simulate a **real-world language tutoring experience**, ensuring that models provide **progressive learning** rather than just direct corrections.

#### Key Design Choices & Intentions

✔️ **Minimal Input (Zero-Shot Learning)** – The prompt was kept **intentionally simple** to assess the models' **baseline capabilities** with minimal guidance.  
✔️ **No Examples Given** – To avoid biasing the response, the models were tested in a **zero-shot setting**, meaning no sample corrections were provided.  
✔️ **First-Person Framing** – The use of **first-person language ("You are my tutor... I will write a sentence...")** was intentional to make the interaction feel **more natural** when using a pre-trained model in a simple chat interface.  
✔️ **Encourages Active Learning** – Instead of giving direct answers, the model nudges the learner toward self-correction.  
✔️ **Provides Structured Feedback** – Identifies **error types** (e.g., grammar, syntax, word choice) and offers **hints** before revealing answers.  
✔️ **Ensures Consistency Across Languages** – The same approach was applied to **Portuguese, French, English, and Spanish** to evaluate cross-language adaptability.  
✔️ **Maintains a Friendly & Supportive Tone** – Encourages engagement and motivation for language learners.  
✔️ **Simulates a Real Tutoring Approach** – Encourages retries and only reveals the full correction if necessary.  

📌 **Note:** The `[target language]` placeholder was replaced for each test with the corresponding language.

## Results

This section presents the performance of **4o** and **o1** models across different languages and proficiency levels. Each test followed the same methodology, evaluating **feedback quality, pedagogical value, and response consistency**.

### Portuguese (Beginner Level)

#### Test Sentence (PT)

📝 *Meu filho vai a escola todos os dias.*  
✔️ Corrected: *Meu filho vai à escola todos os dias.*  
💬 *"My son goes to school every day."*

#### 4o Model Response (PT)

✅ Identified the preposition error and provided an explanation.  
❌ Inconsistent behavior—sometimes gave hints, other times the full answer.  

#### o1 Model Response (PT)

✅ Responded in **Portuguese**, assuming student proficiency.  
✅ Provided **structured feedback** and hints without revealing the answer.  
❌ **Slower response time** (~20 sec).  

#### Portuguese Prompt – 4o vs. o1 Model Responses

| **4o Model Response** | **o1 Model Response** |
|----------------------|----------------------|
| [![4o Portuguese Prompt](https://drive.google.com/thumbnail?id=1hPcz24_xAW0ZhPJYLCspxL9nVFVaOpnv)](https://drive.google.com/file/d/1hPcz24_xAW0ZhPJYLCspxL9nVFVaOpnv/view?usp=sharing) | [![o1 Portuguese Prompt](https://drive.google.com/thumbnail?id=1uYZhnVMUoBJzAjvk3WsZAdAnPCquhpYY)](https://drive.google.com/file/d/1uYZhnVMUoBJzAjvk3WsZAdAnPCquhpYY/view?usp=sharing) |
| *Portuguese Prompt – 4o Model* | *Portuguese Prompt – o1 Model* |

#### Conclusion (PT)

- **o1 was more structured** but slower.  
- **4o was inconsistent** but still useful for quick corrections.  
- The **lack of memory in temporary chats** could explain variations in responses.

### French (Intermediate Level)

#### Test Sentence (FR)

📝 *J'aimerai bien voyager par tout le monde, dégoûter les plusieurs cuisines, et apprendre plusieurs langues.*  
✔️ Corrected: *J'aimerais bien voyager à travers le monde, goûter plusieurs cuisines, et apprendre plusieurs langues.*  
💬 *"I would like to travel around the world, taste many cuisines, and learn many languages."*

#### 4o Model Response (FR)

✅ Identified **four errors** and gave helpful hints.  
✅ Used **friendly tone** with emojis to encourage engagement.  

#### o1 Model Response (FR)

✅ Identified **same four errors** concisely.  
✅ **More professional and precise**, no emojis.  
❌ Responded in **English**, unlike the Portuguese test.  

#### French Prompt – 4o vs. o1 Model Responses

| **4o Model Response** | **o1 Model Response** |
|----------------------|----------------------|
| [![4o French Prompt](https://drive.google.com/thumbnail?id=1kTzMGw7n0sEY9LVI__lBdyAIK_mSE7Te)](https://drive.google.com/file/d/1kTzMGw7n0sEY9LVI__lBdyAIK_mSE7Te/view?usp=sharing) | [![o1 French Prompt](https://drive.google.com/thumbnail?id=1G7JjBw8mPP1JBl_v_L8FQzT_YX8PYVXH)](https://drive.google.com/file/d/1G7JjBw8mPP1JBl_v_L8FQzT_YX8PYVXH/view?usp=sharing) |
| *French Prompt – 4o Model* | *French Prompt – o1 Model* |

#### Conclusion (FR)

- **4o was more engaging** (emojis, casual tone).  
- **o1 was more structured** but lacked the immersive language-learning approach.  
- Both models suggested similar **stylistic improvements** beyond basic corrections.

### English (Advanced Level: Adjective Order Test)

#### Test Sentence (EN)

📝 *Wouldn’t it be lovely to restore a single century-old neglected modest weathered gabled wooden rural faded Japanese akiya to its former glory?*  

#### 4o Model Response (EN)

❌ Missed the **core grammar rule** on adjective order.  
❌ Focused on **sentence length** instead.  
✅ Provided adjective order **only after prompting**.  

#### o1 Model Response (EN)

✅ Recognized the sentence was grammatically correct.  
✅ Provided **hints instead of full answers**, making it more pedagogically valuable.  
✅ Suggested **breaking down long adjective strings for readability**.

#### English Prompt – 4o vs. o1 Model Responses

| **4o Model Response** | **o1 Model Response** |
|----------------------|----------------------|
| [![4o English Prompt](https://drive.google.com/thumbnail?id=1kes-xvkXhRDcGun58cWCeLuJp-WfIKZe)](https://drive.google.com/file/d/1kes-xvkXhRDcGun58cWCeLuJp-WfIKZe/view?usp=sharing) | [![o1 English Prompt](https://drive.google.com/thumbnail?id=1bld1yY9o_Nd1XZskUtMzljTKHvvcdPcH)](https://drive.google.com/file/d/1bld1yY9o_Nd1XZskUtMzljTKHvvcdPcH/view?usp=sharing) |
| *English Prompt – 4o Model* | *English Prompt – o1 Model* |

#### Conclusion (EN)

- **4o struggled to identify the main learning point** and needed extra prompting.  
- **o1 was better at guiding the student** while maintaining a structured approach.  
- This test revealed that **explicitly stating learning goals** in the prompt would improve model responses.

### Spanish (Expert Level: Medical Terminology)

#### Test Sentence (ES)

📝 *El cardiólogo y la intensivista han determinado que, dada tu historia médica, la intervención más adecuada en tu caso es una angioplastia coronaria.*  
✔️ Suggested Improvement: *dado tu historial médico* (better medical terminology).  
💬 *"The cardiologist and the intensivist have determined that, given your medical history, the most appropriate intervention in your case is a coronary angioplasty."*

#### 4o Model Response (ES)

✅ Switched to **Spanish** after detecting user fluency.  
✅ Provided **high-level medical vocabulary improvements**.  

#### o1 Model Response (ES)

✅ Started **directly in Spanish**, similar to the Portuguese test.  
✅ Provided **concise, professional feedback**.  
✅ Warmer tone than in other languages.

#### Spanish Prompt – 4o vs. o1 Model Responses

| **4o Model Response** | **o1 Model Response** |
|----------------------|----------------------|
| [![4o Spanish Prompt](https://drive.google.com/thumbnail?id=1_b_8QT3ij9za8p74nL9ddBq_ORetLru1)](https://drive.google.com/file/d/1_b_8QT3ij9za8p74nL9ddBq_ORetLru1/view?usp=sharing) | [![o1 Spanish Prompt](https://drive.google.com/thumbnail?id=1IhWl2dvW-L8AZ-SE8zg1P6e_q-UkLzEr)](https://drive.google.com/file/d/1IhWl2dvW-L8AZ-SE8zg1P6e_q-UkLzEr/view?usp=sharing) |
| *Spanish Prompt – 4o Model* | *Spanish Prompt – o1 Model* |

#### Conclusion (ES)

- **Both models provided excellent feedback** at an expert level.  
- **o1's response was slightly warmer**, possibly due to **cultural language nuances**.  
- This test confirmed that both models **perform well in specialized, high-proficiency tasks**.

### Overall Observations

✅ **o1 was more structured and professional**, but **slower**.  
✅ **4o was more engaging**, but **less consistent** in responses.  
✅ **Both models adapted well to high-proficiency tasks**, while **4o struggled with lower levels**.  
✅ The **language of response varied**, with **o1 defaulting to English in the French test but Spanish in the expert-level test**.  

## Conclusion & Next Steps

### Key Takeaways

- **o1 was more structured and pedagogically valuable**, making it the better choice for formal language learning.  
- **4o was more engaging but inconsistent**, making it suitable for informal practice but less reliable for structured feedback.  
- **Both models adapted well to expert-level tasks**, but **4o struggled at lower proficiency levels** due to inconsistency.  
- **Language response inconsistency was observed**, with **o1 switching to English in the French test but using Spanish in the expert test.**  
- **o1 was generally slower**, taking up to **20 seconds** for some responses, which may affect real-time learning applications.
- **o1 would likely be more costly**, as its longer response times and structured approach require more computational resources compared to 4o.

### Next Steps & Potential Improvements

- **Test with more languages & levels**  
  - Expanding the study to **German, Italian, and Mandarin** could provide deeper insights into model adaptability.  

- **Refine prompts for better guidance**  
  - Explicitly stating learning goals in the prompt could improve responses, especially for **complex grammar concepts**.  

- **Compare with a memory-enabled chat**  
  - Since **temporary chats prevent context retention**, testing with **persistent memory on** might yield different results.  

- **Investigate latency issues**  
  - **o1 was significantly slower**, raising questions about efficiency in real-world use. Future testing could analyze response time variations.  

- **Explore model fine-tuning for language learning**  
  - If OpenAI allows fine-tuning, adapting the models for **better consistency and structured guidance** could enhance their use for education.

### Final Thoughts

This experiment highlights **the strengths and weaknesses of AI-powered language tutoring**, showing that while **AI models can provide helpful corrections, their effectiveness depends on structure, consistency, and engagement.** Future improvements in **prompt engineering, model selection, and AI memory usage** could lead to a more **reliable** and **interactive** AI-assisted learning experience.
