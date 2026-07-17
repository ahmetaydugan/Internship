## Day-5: Weekly Report

Please find below the comparative analysis report I have prepared regarding the performance and architectural differences between the rule-based (if-else) expert system I developed and the Machine Learning (Decision Tree) model I trained on data.


### Comparative Analysis Report: Rule-Based Systems (If-Else) vs. Machine Learning (Decision Tree)

#### 1. Unexpected Behaviors and Vulnerabilities I Detected in the If-Else Expert System

Upon reviewing the `expert_system` function I developed, I detected that the system exhibits fragility in three core architectural areas:

* **Text Dependency and Loss of Flexibility:** I observed that the text-matching rule I implemented in the code is strictly tied to specific phrases in the log message. If a system update changes the "exhausted" or "node down" message to a different string, the system misses this critical error and defaults to the "ignore" rule.


* **Hardcoded Thresholds:** I noticed that the `> 1000` rule I established for latency lacks logical nuance. I identified that while an operation taking 1001 milliseconds triggers a watch state, one taking 999 milliseconds is classified as entirely normal by the system.
* **Rule Shadowing:** I positioned the condition evaluating `code in [400, 401, 429]` at the top of the hierarchy. As a result, I found that if a service returns a 401 error, the system exits the evaluation block and ignores the event before it can assess the latency, even if the operation took 5000 milliseconds.



#### 2. My Observations on the Resilience of the Decision Tree Against Change

I determined that the decision tree model I trained provides flexibility by evaluating hidden patterns within the data instead of reading static rules from top to bottom:

* **Holistic and Multidimensional Analysis:** I observed that the machine learning model evaluates service type, error code, latency, and log level simultaneously as a matrix. When an error code and high latency occur concurrently, the model dynamically interprets this combination.
* **Abstraction from Text:** I deliberately did not utilize the content of the error message as a structural feature during the model's training phase. Consequently, I verified that even if the error message text changes in the production environment, the model can still execute the correct mathematical classification by analyzing the error code (e.g., 500), severity level (error), and latency.



#### 3. My Deductions on Why Expert Systems Failed to Scale in the 1980s

I consider the `if-else` structure I developed to be a fundamental representation of the "Expert Systems" architecture of the 1980s. I can summarize the primary reasons these systems failed during that era, triggering the "AI Winter," as follows:

* **Maintenance Nightmare:** I realized that when dozens of different services and hundreds of error scenarios are introduced, `if-else` blocks expand to unmanageable sizes. I experienced firsthand that testing whether a newly added rule conflicts with an existing one becomes practically impossible.
* **Inability to Manage Uncertainty:** Real-world data is noisy and imperfect. Because expert systems operate on absolute true/false logic, I determined that they generate erroneous results when confronted with incomplete or unexpected data.

#### 4. The Connection I Established with Modern Rule-Based Monitoring Systems

I identified that this analysis aligns directly with the "Alert Fatigue" problem prevalent in modern DevOps and SRE (Site Reliability Engineering) disciplines.

I observe that the static alerts configured in today's industry-standard observability tools operate on the same logic as 1980s expert systems. I detected that in dynamic cloud environments, these rigid thresholds continuously generate false positives, negatively impacting engineers' reaction times. Therefore, I concluded that modern monitoring architectures must transition from static rules toward Machine Learning systems that perform "Anomaly Detection" by analyzing historical data.
