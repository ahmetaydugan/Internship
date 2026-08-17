## Day 1 - Frequency Analysis and Defining "Normal":
Starting the 7th week of my internship, I transitioned from parsing logs to actively hunting for anomalies. Today was all about analyzing the temporal distribution of the templates I extracted last week and understanding the mathematical philosophy of anomaly detection.

1. Practical Task: Visualizing Template Frequencies
Building on the structured data from last week (which yielded 14 total templates and 2 one-off occurrences), I focused on mapping these templates over time. I plotted the occurrence frequency of each template to observe how they fluctuate across different hours and periods. This visual frequency analysis helped me identify abnormal spikes or unexpected drops in specific log patterns over time, revealing the natural heartbeat of the system.

2. Concept: How Do We Define "Normal" Behavior?
I explored the core philosophy of anomaly detection: how do we actually define what is "normal"? I realized that relying on a fixed threshold (e.g., "alert if an event happens more than 50 times") is highly ineffective because system traffic naturally fluctuates depending on the time of day or user load. Instead, "normal" must be defined using a statistical range or a dynamic baseline (like moving averages or standard deviations). An anomaly isn't simply hitting a hard, pre-defined limit; it is a statistically significant deviation from the expected, dynamic rhythm of the system.
