## Day 4 - Rule-Based vs. Learning-Based Comparison:
Wrapping up the core analytical phase of the anomaly detection pipeline, today I stepped back to evaluate the structural methodology itself, comparing the rigidity of static rules against the adaptability of dynamic learning.

1. Concept: Fixed Thresholds vs. Adaptive Baselines
Drawing a parallel to the Expert Systems vs. Decision Trees analysis I conducted back in Week 2, I compared rule-based anomaly detection (fixed thresholds) against statistical/learning-based approaches. A fixed rule (like a hardcoded limit) is fast and easy to implement, but it is entirely rigid—it triggers false alarms the moment system traffic naturally increases due to normal business cycles. Conversely, a statistical approach dynamically adapts to the "normal" rhythm of the system, learning the baseline. While it requires historical data and heavier computation, it is vastly more resilient to organic changes in the environment.

2. Practical Task: The Controlled Threshold Experiment
To observe this theoretical difference in action, I set up a controlled experiment. I manipulated a single variable: the sensitivity threshold for anomaly detection. I ran the exact same parsed log dataset first with a strict fixed threshold, then with a statistical multiplier (mean + 2 standard deviations), and finally increased the multiplier to 3.

The results were eye-opening: a low, static threshold caused severe "alert fatigue" by generating too many false positives, while an overly high multiplier resulted in false negatives, completely missing actual system spikes. This mathematically proved that relying on a static rule is unsustainable in a dynamic production environment; true intelligence requires adaptive, learning-based thresholds.
