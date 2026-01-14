#Functions were created with AI's help
import os
import networkx as nx
import matplotlib.pyplot as plt

from utils.fileUtils import get_words_from_file, save_words_to_file, save_similarity_matrix
from utils.translate import translate_words
from utils.similarity import compute_similarity
from utils.overall_similarity import diagonal_average, add_connection

# Language mapping - full names to language codes
LANGUAGE_MAP = {
    "afrikaans": "af",
    "albanian": "sq",
    "basque": "eu",
    "catalan": "ca",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dutch": "nl",
    "english": "en",
    "estonian": "et",
    "finnish": "fi",
    "french": "fr",
    "galician": "gl",
    "german": "de",
    "hungarian": "hu",
    "icelandic": "is",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "latin": "la",
    "latvian": "lv",
    "lithuanian": "lt",
    "malay": "ms",
    "maltese": "mt",
    "norwegian": "no",
    "polish": "pl",
    "portuguese": "pt",
    "romanian": "ro",
    "slovak": "sk",
    "slovenian": "sl",
    "spanish": "es",
    "swahili": "sw",
    "swedish": "sv",
    "tagalog": "tl",
    "turkish": "tr",
    "vietnamese": "vi",
    "welsh": "cy"
}


def display_available_languages():
    """Display all available languages in a formatted way"""
    print("\n" + "=" * 60)
    print("AVAILABLE LANGUAGES:")
    print("=" * 60)

    languages_list = sorted(LANGUAGE_MAP.keys())
    # Display in 3 columns
    for i in range(0, len(languages_list), 3):
        row = languages_list[i:i + 3]
        print("  ".join(f"{lang.capitalize():<20}" for lang in row))
    print("=" * 60)


def get_language_code(language_name):
    """
    Convert language name to language code (case-insensitive)
    Returns language code or None if not found
    """
    return LANGUAGE_MAP.get(language_name.lower().strip())


def select_languages():
    """
    Let user select 2-4 languages for comparison
    Returns list of language codes
    """
    display_available_languages()

    while True:
        print("\nPlease enter 2-4 languages you want to compare.")
        print("Separate them with commas (e.g., English, Spanish, Polish)")
        print("Type 'list' to see available languages again")

        user_input = input("\nYour selection: ").strip()

        if user_input.lower() == 'list':
            display_available_languages()
            continue

        # Split by comma and clean up
        language_names = [lang.strip() for lang in user_input.split(',')]

        # Validate number of languages
        if len(language_names) < 2:
            print("❌ Error: Please select at least 2 languages.")
            continue

        if len(language_names) > 4:
            print("❌ Error: Please select maximum 4 languages.")
            continue

        # Convert to language codes
        language_codes = []
        invalid_languages = []

        for lang_name in language_names:
            code = get_language_code(lang_name)
            if code:
                language_codes.append(code)
            else:
                invalid_languages.append(lang_name)

        # Check if all languages are valid
        if invalid_languages:
            print(f"❌ Error: Unknown language(s): {', '.join(invalid_languages)}")
            print("Please check the spelling and try again, or type 'list' to see available languages.")
            continue

        # Check for duplicates
        if len(language_codes) != len(set(language_codes)):
            print("❌ Error: You selected the same language multiple times.")
            continue

        # Success!
        selected_names = [name.capitalize() for name in language_names]
        print(f"\n✅ Selected languages: {', '.join(selected_names)}")
        return language_codes


def process_word_file(file_path, languages, results_dir):
    """
    Process a single word file and generate translations, similarities, and graph
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist!")
        return False

    if not file_path.endswith(".txt"):
        print(f"Warning: File should be a .txt file. Continuing anyway...")

    # Extract topic name from filename
    topic = os.path.splitext(os.path.basename(file_path))[0]
    print(f"\n=== Processing topic: {topic} ===")

    G = nx.Graph()  # Graph will be stored here

    try:
        words = get_words_from_file(file_path)
        print(f"Loaded {len(words)} words from {os.path.basename(file_path)}")

        if len(words) == 0:
            print("Error: No words found in the file!")
            return False

        # Translate words to all selected languages
        print("Translating words...")
        translations = {lang: translate_words(words, lang) for lang in languages}

        # Save translations
        for lang, trans_words in translations.items():
            save_words_to_file(trans_words, f"{results_dir}/translations/{topic}_{lang}.txt")
        print("Translations saved.")

        # Compute similarities and build graph
        print("Computing similarities...")
        for i in range(len(languages)):
            for j in range(i + 1, len(languages)):
                lang1, lang2 = languages[i], languages[j]
                matrix = [[compute_similarity(w1, w2) for w2 in translations[lang2]]
                          for w1 in translations[lang1]]
                save_similarity_matrix(translations[lang1], translations[lang2], matrix,
                                       f"{results_dir}/similarities/{topic}_{lang1}_{lang2}.csv")

                # Add connection to graph
                outcome = diagonal_average(matrix) * 100
                add_connection(G, lang1, lang2, f"{round(outcome, 2)}%")

        # Draw and save graph
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"))

        # Create title with language names
        lang_names = [list(LANGUAGE_MAP.keys())[list(LANGUAGE_MAP.values()).index(code)].capitalize()
                      for code in languages]
        plt.title(f"{topic} - Word Similarity ({', '.join(lang_names)})")

        graph_path = f"{results_dir}/{topic}_similarity_graph.png"
        plt.savefig(graph_path, format="png", dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Graph saved to: {graph_path}")

        return True

    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return False


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 60)
    print("Step 2: File Selection")
    print("=" * 60)
    print("\nOptions:")
    print("1. Analyze a single file")
    print("2. Analyze all files in a directory")
    print("3. Change language selection")
    print("4. Exit")


def get_file_path():
    """Get file path from user"""
    file_path = input("\nEnter the full path to your word file (.txt): ").strip()
    # Remove quotes if user copied path with quotes
    return file_path.strip('"').strip("'")


def get_directory_path():
    """Get directory path from user"""
    dir_path = input("\nEnter the directory path containing .txt files: ").strip()
    return dir_path.strip('"').strip("'")


def process_directory(dir_path, languages, results_dir):
    """Process all .txt files in a directory"""
    if not os.path.exists(dir_path):
        print(f"Error: Directory '{dir_path}' does not exist!")
        return

    if not os.path.isdir(dir_path):
        print(f"Error: '{dir_path}' is not a directory!")
        return

    txt_files = [f for f in os.listdir(dir_path) if f.endswith(".txt")]

    if not txt_files:
        print("No .txt files found in the directory!")
        return

    print(f"\nFound {len(txt_files)} .txt file(s). Processing...")

    success_count = 0
    for filename in txt_files:
        file_path = os.path.join(dir_path, filename)
        if process_word_file(file_path, languages, results_dir):
            success_count += 1

    print(f"\n✅ Successfully processed {success_count}/{len(txt_files)} files!")