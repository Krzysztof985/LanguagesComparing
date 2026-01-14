#unit tests were created with AI's help
import unittest
import os
import tempfile
import shutil
import csv
from unittest.mock import patch, MagicMock

# Import your modules
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.translate import translate_word, translate_words
from src.utils.fileUtils import get_words_from_file, save_words_to_file, save_similarity_matrix
from src.utils.similarity import compute_similarity
from src.utils.overall_similarity import diagonal_average, add_connection



class TestFileUtils(unittest.TestCase):
    """Test suite for fileUtils.py"""

    def setUp(self):
        """Create a temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the temporary directory after tests"""
        shutil.rmtree(self.test_dir)

    def test_get_words_from_file(self):
        """Test reading words from a file"""
        test_file = os.path.join(self.test_dir, "test_words.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("apple\nbanana\ncherry\n")

        words = get_words_from_file(test_file)
        self.assertEqual(words, ["apple", "banana", "cherry"])

    def test_get_words_from_file_with_empty_lines(self):
        """Test reading words with empty lines"""
        test_file = os.path.join(self.test_dir, "test_words.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("apple\n\nbanana\n  \ncherry\n")

        words = get_words_from_file(test_file)
        self.assertEqual(words, ["apple", "banana", "cherry"])

    def test_save_words_to_file(self):
        """Test saving words to a file"""
        words = ["dog", "cat", "bird"]
        test_file = os.path.join(self.test_dir, "output", "saved_words.txt")

        save_words_to_file(words, test_file)

        # Verify file was created
        self.assertTrue(os.path.exists(test_file))

        # Verify content
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read().strip().split("\n")
        self.assertEqual(content, words)

    def test_save_similarity_matrix(self):
        """Test saving similarity matrix to CSV"""
        words1 = ["hello", "world"]
        words2 = ["hola", "mundo"]
        matrix = [[0.85, 0.32], [0.28, 0.91]]
        test_file = os.path.join(self.test_dir, "matrix", "test_matrix.csv")

        save_similarity_matrix(words1, words2, matrix, test_file)

        # Verify file exists
        self.assertTrue(os.path.exists(test_file))

        # Verify content
        with open(test_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(rows[0], ["", "hola", "mundo"])
        self.assertEqual(rows[1][0], "hello")
        self.assertEqual(rows[2][0], "world")


class TestSimilarity(unittest.TestCase):
    """Test suite for similarity.py"""

    def test_compute_similarity_identical(self):
        """Test similarity of identical words"""
        similarity = compute_similarity("hello", "hello")
        self.assertEqual(similarity, 1.0)

    def test_compute_similarity_completely_different(self):
        """Test similarity of completely different words"""
        similarity = compute_similarity("abc", "xyz")
        self.assertEqual(similarity, 0.0)

    def test_compute_similarity_partial(self):
        """Test similarity of partially similar words"""
        similarity = compute_similarity("kitten", "sitting")
        self.assertGreater(similarity, 0.0)
        self.assertLess(similarity, 1.0)

    def test_compute_similarity_case_sensitive(self):
        """Test that similarity is case-sensitive"""
        sim1 = compute_similarity("Hello", "hello")
        sim2 = compute_similarity("hello", "hello")
        self.assertNotEqual(sim1, sim2)


class TestOverallSimilarity(unittest.TestCase):
    """Test suite for overall_similarity.py"""

    def test_diagonal_average_square_matrix(self):
        """Test diagonal average with square matrix"""
        matrix = [
            [1.0, 0.5, 0.3],
            [0.5, 1.0, 0.6],
            [0.3, 0.6, 1.0]
        ]
        avg = diagonal_average(matrix)
        self.assertEqual(avg, 1.0)

    def test_diagonal_average_non_square_matrix(self):
        """Test diagonal average with non-square matrix"""
        matrix = [
            [0.8, 0.5, 0.3, 0.2],
            [0.5, 0.9, 0.6, 0.1],
            [0.3, 0.6, 0.7, 0.4]
        ]
        avg = diagonal_average(matrix)
        expected = (0.8 + 0.9 + 0.7) / 3
        self.assertAlmostEqual(avg, expected)

    def test_diagonal_average_empty_matrix(self):
        """Test diagonal average with empty matrix"""
        matrix = []
        avg = diagonal_average(matrix)
        self.assertEqual(avg, 0)

    def test_add_connection(self):
        """Test adding connection to graph"""
        import networkx as nx
        G = nx.Graph()

        add_connection(G, "en", "pl", 85.5)

        self.assertTrue(G.has_node("en"))
        self.assertTrue(G.has_node("pl"))
        self.assertTrue(G.has_edge("en", "pl"))
        self.assertEqual(G["en"]["pl"]["label"], 85.5)


class TestTranslate(unittest.TestCase):
    """Test suite for translate.py"""

    @patch('src.utils.translate.GoogleTranslator')
    def test_translate_word_success(self, mock_translator):
        """Test successful word translation"""
        mock_instance = MagicMock()
        mock_instance.translate.return_value = "Hola"
        mock_translator.return_value = mock_instance

        result = translate_word("hello", "es")

        self.assertEqual(result, "hola")
        mock_translator.assert_called_once_with(source='auto', target='es')
        mock_instance.translate.assert_called_once_with("hello")

    @patch('src.utils.translate.GoogleTranslator')
    def test_translate_word_error(self, mock_translator):
        """Test word translation error handling"""
        mock_instance = MagicMock()
        mock_instance.translate.side_effect = Exception("Translation error")
        mock_translator.return_value = mock_instance

        result = translate_word("hello", "es")

        # Should return original word on error
        self.assertEqual(result, "hello")

    @patch('src.utils.translate.translate_word')
    def test_translate_words(self, mock_translate):
        """Test translating multiple words"""
        mock_translate.side_effect = lambda w, l: f"{w}_translated"

        words = ["hello", "world", "test"]
        result = translate_words(words, "es")

        expected = ["hello_translated", "world_translated", "test_translated"]
        self.assertEqual(result, expected)
        self.assertEqual(mock_translate.call_count, 3)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full workflow"""

    def setUp(self):
        """Create a temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Remove the temporary directory after tests"""
        shutil.rmtree(self.test_dir)

    def test_similarity_matrix_creation(self):
        """Test creating a similarity matrix between word lists"""
        words_en = ["hello", "world"]
        words_es = ["hola", "mundo"]

        matrix = [[compute_similarity(w1, w2) for w2 in words_es] for w1 in words_en]

        # Check matrix dimensions
        self.assertEqual(len(matrix), 2)
        self.assertEqual(len(matrix[0]), 2)

        # Check all values are between 0 and 1
        for row in matrix:
            for val in row:
                self.assertGreaterEqual(val, 0.0)
                self.assertLessEqual(val, 1.0)

    def test_full_workflow_with_files(self):
        """Test the complete workflow from file to results"""
        # Create test input file
        input_file = os.path.join(self.test_dir, "test_words.txt")
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("hello\nworld\n")

        # Read words
        words = get_words_from_file(input_file)
        self.assertEqual(len(words), 2)

        # Create output file
        output_file = os.path.join(self.test_dir, "output", "processed.txt")
        save_words_to_file(words, output_file)

        # Verify output
        self.assertTrue(os.path.exists(output_file))
        saved_words = get_words_from_file(output_file)
        self.assertEqual(words, saved_words)


def run_tests():
    """Run all tests with verbose output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFileUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestSimilarity))
    suite.addTests(loader.loadTestsFromTestCase(TestOverallSimilarity))
    suite.addTests(loader.loadTestsFromTestCase(TestTranslate))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    result = run_tests()

    # Print summary
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 70)