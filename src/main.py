import os
from src.displayUtils import (
    select_languages,
    process_word_file,
    display_menu,
    get_file_path,
    get_directory_path,
    process_directory
)

# Get the project root directory (parent of src)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(project_root, "results")

# Create necessary directories
os.makedirs(f"{results_dir}/translations", exist_ok=True)
os.makedirs(f"{results_dir}/similarities", exist_ok=True)


def main():
    print("=" * 60)
    print("Word Similarity Analyzer - Levenshtein Method")
    print("=" * 60)

    # Step 1: Language Selection
    print("\nStep 1: Language Selection")
    languages = select_languages()

    # Main loop
    while True:
        display_menu()

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            # Analyze single file
            file_path = get_file_path()

            if process_word_file(file_path, languages, results_dir):
                print("\n✅ File processed successfully!")
            else:
                print("\n❌ Failed to process file.")

        elif choice == "2":
            # Analyze directory
            dir_path = get_directory_path()
            process_directory(dir_path, languages, results_dir)

        elif choice == "3":
            # Change language selection
            print("\n" + "=" * 60)
            print("Changing language selection...")
            print("=" * 60)
            languages = select_languages()

        elif choice == "4":
            # Exit
            print("\nExiting. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()