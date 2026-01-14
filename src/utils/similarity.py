import textdistance

"""
   Calculate normalized similarity between two words using Levenshtein distance.

   Args:
       word1 (str): First word
       word2 (str): Second word

   Returns:
       float: Similarity score between 0.0 (completely different) and 1.0 (identical)

   Example:
       >>> compute_similarity("cat", "cat")
       1.0
       >>> compute_similarity("cat", "dog")
       0.0
       >>> compute_similarity("kitten", "sitting")
       0.571  # approximately
   """
def compute_similarity(word1, word2):
    return textdistance.levenshtein.normalized_similarity(word1, word2)