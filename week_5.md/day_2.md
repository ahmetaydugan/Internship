## Day 2 - Similarity Search and Retrieval:
On the second day of the week, I transitioned from simply creating static vector embeddings to actively using them to build the foundation of a semantic search engine. Today was entirely focused on the "Retrieval" aspect of RAG.

1. Concept: The Logic of Nearest Neighbor Search
I started by diving into the mathematics of Nearest Neighbor search. I learned how converting a user's question into an embedding allows us to map it into the exact same vector space as our document chunks. By calculating the distances in this space, we can easily identify and extract the top k documents that are mathematically closest to the question, meaning they are the most semantically relevant.

2. Infrastructure: Vector Databases and FAISS
Next, I explored the concept of vector databases, which are designed to handle these similarity searches at a massive scale. I learned what FAISS (Facebook AI Similarity Search) is and why it is absolutely critical for efficiently searching through millions of embeddings. However, I also realized that for my current, small-scale dataset, a simple numpy array combined with a cosine similarity function is perfectly sufficient and much lighter to run.

3. Practical Coding: Building the Retrieval System
For the practical task, I turned yesterday's document set into a mini "knowledge base." I wrote a specific question, converted it into an embedding, and used cosine similarity to find and return the top 3 most relevant document chunks. I deliberately kept Large Language Models (LLMs) out of the equation today. My sole focus was on proving that the system could successfully retrieve the correct context based purely on meaning.
