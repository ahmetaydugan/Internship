## Day 2 - Drain3 Installation and First Template Extraction:
On the second day of my sixth week, I moved from manual log inspection to automated parsing, learning how to algorithmically extract structured templates from chaotic raw system logs.

1. Concept: The Mechanics of Drain3
I studied the operational logic of the Drain3 algorithm. I learned how it builds a parse tree, separates static text tokens from dynamic variables, and uses a similarity threshold to cluster logs. Rather than diving into the heavy underlying mathematics, I focused on gaining a solid, high-level understanding of how it effectively groups similar logs together in a production environment.

2. Practical Coding: Running Drain3 on HDFS Data
I installed the library using pip install drain3 and executed it on the HDFS_2k.log dataset I manually analyzed yesterday. I closely observed how the algorithm processed each raw log line and successfully mapped it to a specific template. To take it a step further, I tracked and counted exactly how many actual log lines were represented by each individual template.

3. Output: Template Analysis and Terminal Results
The algorithm successfully parsed the entire file. I extracted the total number of unique templates found and identified the top 5 most frequently occurring templates in the dataset. I formatted and saved these metrics as a clean terminal output, perfectly demonstrating the transformation from unstructured text to structured, quantifiable data.
