## Day 3 - From BERT to ChatGPT:
On the third day of my fourth week, I traced the rapid evolution of large language models, moving from static embeddings to conversational agents. Today was as much about understanding the history of scaling and alignment as it was about learning professional development habits.

1. Historical Analysis: BERT, Scaling Laws, and RLHF
I studied the trajectory from 2018's BERT, which introduced bidirectional reading, to the evolution of the GPT series. I explored the "scaling laws"—the observation that simply increasing model size and data volume leads to predictable performance gains—from GPT-2 to GPT-3. Finally, I examined 2022's ChatGPT and the introduction of Reinforcement Learning from Human Feedback (RLHF). Learning how models are fine-tuned to be "helpful" using human feedback bridged the gap between raw text prediction and the conversational AI we use today.

2. Practical Coding: First API Call
I set up my free API key to start interacting with these models programmatically. I chose Google AI Studio (Gemini) for this task. After configuring the environment, I successfully made my first API call. Seeing the model generate a response based on my own code felt like unlocking a new level of control, moving from simply running models locally to integrating intelligence into my own applications.

3. The Critical Habit: API Security
Today's most important lesson wasn't about AI architecture, but about developer hygiene. I learned the essential rule of API security: never hardcode credentials. I created a .env file to store my API key, added it to my .gitignore file, and verified that my secrets would never be committed to the repository. This is the "hidden lesson" of the week, and it is crucial for ensuring that my code remains secure and professional.
