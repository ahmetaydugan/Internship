## Day 4 - Testing the Limits of RAG:
On the fourth day of my fifth week, I pushed my newly built RAG pipeline to its limits to see exactly where it breaks. Today was about understanding that RAG is not a magic wand and testing how to properly constrain a language model in production.

1. The Experiment: Pushing for Hallucinations
I conducted a stress test by asking my Groq-powered RAG application a question about a topic completely absent from my custom document set. I carefully observed the model's behavior. Because the retrieved context didn't contain the answer, the model fell back on its pre-trained general knowledge and started hallucinating, confidently generating an answer that wasn't grounded in my specific knowledge base.

2. Practical Fix: System Prompt Engineering
To fix this vulnerability, I modified the system prompt passed to the Groq client, adding a strict constraint: "Only answer based on the provided context. If the context does not contain the answer, say 'I do not have this information'." I ran the exact same query again and compared the difference. This time, the model perfectly obeyed the boundary and safely admitted its lack of knowledge instead of guessing.

3. The "Wall" and the Key Takeaway
Hitting this structural "wall" was my biggest lesson today. Even with a sophisticated RAG architecture, if the system isn't given strict operational boundaries through prompting, it will still hallucinate. This hands-on experiment perfectly encapsulates the limitations of AI.
