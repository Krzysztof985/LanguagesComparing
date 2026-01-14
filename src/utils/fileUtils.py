import os
import csv

def get_words_from_file(file_path):
    """
       Read words from a text file, one word per line.

       Args:
           file_path (str): Path to the input text file

       Returns:
           list: List of words with whitespace stripped, empty lines removed

       Example:
           >>> words = get_words_from_file("data/animals.txt")
           >>> print(words)
           ['dog', 'cat', 'bird']
       """
    with open(file_path, "r", encoding="utf-8") as f:
        return [w.strip() for w in f.readlines() if w.strip()]

def save_words_to_file(words, file_path):
    """
      Save a list of words to a text file, one word per line.
      Creates parent directories if they don't exist.

      Args:
          words (list): List of words to save
          file_path (str): Destination file path

      Returns:
          None

      Example:
          >>> words = ['perro', 'gato', 'pájaro']
          >>> save_words_to_file(words, "results/translations/animals_es.txt")
      """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for w in words:
            f.write(w + "\n")

def save_similarity_matrix(words1, words2, matrix, file_path):
    """
    Save a similarity matrix to a CSV file.
    Rows represent words1, columns represent words2.

    Args:
        words1 (list): List of words for rows
        words2 (list): List of words for columns
        matrix (list of lists): 2D similarity matrix (values 0.0-1.0)
        file_path (str): Destination CSV file path

    Returns:
        None

    Example:
        >>> words_en = ['dog', 'cat']
        >>> words_es = ['perro', 'gato']
        >>> matrix = [[0.85, 0.32], [0.28, 0.91]]
        >>> save_similarity_matrix(words_en, words_es, matrix,
        ...                        "results/similarities/animals_en_es.csv")
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + words2)  # nagłówki kolumn
        for w1, row in zip(words1, matrix):
            writer.writerow([w1] + [f"{v:.2f}" for v in row])