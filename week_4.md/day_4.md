## Day 4 - Hallucinations, Intro to RAG, and Production Awareness:
On the fourth day of my fourth week, I explored the open-source model ecosystem, addressed the hallucination problem, and built a Python CLI tool that tracks API performance metrics under production simulation rules.

1. Concept: Open Models, Hallucinations, and the Need for RAG
I explored the open-source model ecosystem, familiarizing myself with prominent names like Llama and Mistral. I then dived into the "hallucination" problem—understanding why large language models sometimes confidently state incorrect information. To address this, I got a brief preview of RAG (Retrieval-Augmented Generation), which will be next week's main topic, focusing purely on why grounding models in factual, external knowledge is strictly necessary.

2. Practical Coding: CLI Tool for Summarization and Categorization
I developed a Python-based Command Line Interface (CLI) application designed to summarize and categorize text. I utilized the fetch_20newsgroups() dataset from scikit-learn to feed the model real text data. I ensured the output of this tool was meticulously formatted and logged, as these technical reports are reviewed directly by my academic advisor.

3. Production Awareness: Performance Monitoring and Cost Optimization
Moving beyond just making basic API calls, I implemented a performance monitoring tool. I ran an automated batch test of 20-30 requests, carefully logging the input/output token counts and response latency for each run. I then calculated the average token usage and latency. Finally, I projected the daily cost if this system handled one million requests per day using current enterprise API pricing. To mitigate these hypothetical costs, I proposed concrete optimization strategies such as prompt shortening, implementing a caching layer, using smaller models, and request batching.
