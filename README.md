# Word Similarity Analyzer - Levenshtein Method

A Python-based tool designed to analyze linguistic similarities between different languages using the Levenshtein distance method. The application translates word lists into multiple target languages, calculates similarity scores, and generates a visual relationship graph showing the overall similarity between the selected languages.

---

## 🚀 Features

* **Multi-Language Comparison**: Support for 37 different languages including English, Spanish, Polish, Latin, and many others.
* **Automatic Translation**: Uses Google Translator to automatically generate word lists for comparison.
* **Similarity Scoring**: Calculates a normalized similarity score between 0.0 (different) and 1.0 (identical) using the Levenshtein distance.
* **Data Export**:
    * Saves translations to text files.
    * Generates CSV similarity matrices for word-by-word comparison.
    * Outputs language similarity matrices in CSV format for graphing.
* **Visual Graphs**: Generates PNG graphs illustrating the similarity percentages between chosen languages using NetworkX and Matplotlib.

---

## 📂 Project Structure

* `main.py`: The entry point of the application, handling the user interface and main execution loop.
* `displayUtils.py`: Manages language selection, menu displays, and the logic for processing word files and generating graphs.
* `translate.py`: Handles word-by-word and list-based translation using the `deep-translator` library.
* `similarity.py`: Contains the logic for calculating normalized Levenshtein similarity.
* `fileUtils.py`: Provides utility functions for reading/writing text files and saving CSV matrices.
* `overall_similarity.py`: Calculates the average similarity across word lists and manages graph node connections.
* `graphUtils.py`: Provides functions to save language-level similarity matrices in CSV format.

---

## 🛠️ Installation

1. **Ensure you have Python installed.**
2. **Install the required dependencies:**
   ```bash
   pip install textdistance deep-translator networkx matplotlib

📋 UsagePrepare a source file: Create a .txt file containing one word per line (e.g., animals.txt).
Run the script:Bashpython main.py
Step 1: Select Languages: Choose between 2 and 4 languages to compare (e.g., "English, Spanish, Italian").

Step 2: Analyze:Choose Option 1 to process a single file by providing its path.Choose Option 2 to process all .txt files within a specific directory.

Review Results: Results are automatically saved in the results/ directory:results/translations/: Translated word lists.results/similarities/: Word-by-word similarity CSVs.results/[topic]_similarity_graph.png: The visual graph showing percentage similarities.

🧮 Calculation Methodology

Word Similarity: The similarity between two words is calculated as a normalized Levenshtein distance, where 1.0 is a perfect match and 0.0 is entirely different.

Overall Language Similarity: The overall similarity between two languages is determined by the diagonal average of the similarity matrix. This approach specifically compares the similarity of the i-th word in Language A with the i-th translated word in Language B.
