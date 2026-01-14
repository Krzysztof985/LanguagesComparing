from deep_translator import GoogleTranslator

def translate_word(word, lang):
    """
       Translate a single word to the target language.

       Args:
           word (str): Word to translate
           lang (str): Target language code (e.g., 'es', 'fr', 'de')

       Returns:
           str: Translated word in lowercase, or original word if translation fails

       Example:
           >>> translate_word("hello", "es")
           'hola'
           >>> translate_word("cat", "fr")
           'chat'
       """
    try:
        return GoogleTranslator(source='auto', target=lang).translate(word).lower()
    except Exception as e:
        print(f"Error translating {word} to {lang}: {e}")
        return word

def translate_words(words, lang):
    """
        Translate a list of words to the target language.

        Args:
            words (list): List of words to translate
            lang (str): Target language code (e.g., 'es', 'fr', 'de')

        Returns:
            list: List of translated words in the same order

        Example:
            >>> words = ["hello", "world", "cat"]
            >>> translate_words(words, "es")
            ['hola', 'mundo', 'gato']
        """
    return [translate_word(w, lang) for w in words]