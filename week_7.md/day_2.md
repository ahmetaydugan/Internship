## Day 2 - Statistical Threshold Method:
On the second day of the 7th week, I moved from visual frequency analysis to implementing concrete mathematical techniques for anomaly detection. Today was about using statistics to draw the line between normal fluctuations and actual system issues.

1. Concept: Mean, Standard Deviation, and Anomaly Candidates
I focused on the mathematics of baseline creation by calculating the mean occurrence frequency and the standard deviation for each individual log template. By applying basic statistical rules, I learned to define an "anomaly candidate" as any time window where a template's frequency deviates significantly from its norm—specifically, when it exceeds the threshold of the mean plus two standard deviations. This approach provided a solid, math-backed boundary to identify true irregularities rather than just guessing.

2. Practical Coding: Threshold-Based Detection Function
For my practical task, I wrote a Python function that implements this threshold-based anomaly detection logic. I fed my structured template data into the script, instructing it to calculate the statistics and flag the outliers. The function successfully processed the data, identified the time windows that breached the calculated thresholds, and generated a clean list of specific anomalies for further investigation.
