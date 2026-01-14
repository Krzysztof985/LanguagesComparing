import csv
import os

def save_similarity_matrix_csv(matrix, languages, topic, folder="results/graphs"):
    """
        Save a language similarity matrix to CSV format.

        Args:
            matrix (list of lists): 2D matrix of similarity values
            languages (list): List of language codes
            topic (str): Topic name for the file
            folder (str, optional): Output folder path. Defaults to "results/graphs"

        Returns:
            None

        Example:
            >>> matrix = [[1.0, 0.85], [0.85, 1.0]]
            >>> languages = ["en", "es"]
            >>> save_similarity_matrix_csv(matrix, languages, "animals")
        """
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, f"{topic}_matrix.csv")
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + languages)
        for lang, row in zip(languages, matrix):
            writer.writerow([lang] + row)