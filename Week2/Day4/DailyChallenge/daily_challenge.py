import os
import re
import string

try:
    import nltk
    from nltk.corpus import stopwords
    try:
        STOP_WORDS = set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords")
        from nltk.corpus import stopwords
        STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = {
        "a", "an", "the", "and", "or", "but", "if", "then", "else", "when", "while",
        "of", "to", "in", "on", "at", "for", "from", "by", "with", "about", "as",
        "is", "am", "are", "was", "were", "be", "been", "being",
        "it", "its", "itself", "this", "that", "these", "those",
        "he", "she", "they", "them", "his", "her", "their", "we", "us", "you", "your",
        "i", "me", "my", "mine", "ours", "yours", "hers", "theirs",
        "do", "does", "did", "doing", "done", "not", "no", "nor",
        "so", "than", "too", "very", "can", "could", "should", "would", "may", "might",
        "will", "just", "also", "because", "into", "over", "under", "again", "further",
        "up", "down", "out", "off", "only", "own", "same", "such", "both", "each", "few",
        "more", "most", "other", "some", "any", "all", "once"
    }


# =========================
# Part I: Text (analysis)
# =========================
class Text:
    def __init__(self, text: str):
        if not isinstance(text, str):
            raise TypeError(
                f"Expected a string for 'text', got {type(text).__name__}")
        self.text = text.strip()

    def __repr__(self):
        return f"Text({self.text!r})"

    def __str__(self):
        return self.text

    def word_frequency(self, word: str):
        if not isinstance(word, str):
            raise TypeError(
                f"Expected a string for 'word', got {type(word).__name__}")
        translator = str.maketrans("", "", string.punctuation)
        words = self.text.lower().translate(translator).split()
        target = word.lower()
        count = words.count(target)
        return f"'{word}' not found in text." if count == 0 else count

    def most_common_word(self):
        if not self.text:
            return "The text is empty."
        translator = str.maketrans("", "", string.punctuation)
        words = self.text.lower().translate(translator).split()
        frequencies = {}
        for w in words:
            frequencies[w] = frequencies.get(w, 0) + 1
        most_common = max(frequencies, key=frequencies.get)
        return most_common

    def unique_words(self):
        if not self.text:
            return []
        translator = str.maketrans("", "", string.punctuation)
        words = self.text.lower().translate(translator).split()
        return sorted(set(words))

    @classmethod
    def from_file(cls, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {e}")
        return cls(content)


# =========================
# Bonus: TextModification (cleaning)
# =========================
class TextModification(Text):
    def __init__(self, text: str):
        super().__init__(text)

    def remove_punctuation(self):
        punct_class = re.escape(string.punctuation)
        cleaned = re.sub(rf"[{punct_class}]", " ", self.text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        self.text = cleaned
        return self.text

    def remove_stop_words(self):
        words = self.text.split()
        kept = [w for w in words if w.lower() not in STOP_WORDS]
        self.text = " ".join(kept)
        return self.text

    def remove_special_characters(self):
        cleaned = re.sub(r"[^A-Za-z0-9\s]", " ", self.text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        self.text = cleaned
        return self.text


def banner(title: str):
    print("\n" + "=" * 16 + f" {title} " + "=" * 16)


def show_step(title: str, before: str, after: str):
    banner(title)
    print("-- BEFORE --")
    print(before)
    print("\n-- AFTER --")
    print(after)
    print("=" * (36 + len(title)) + "\n")


if __name__ == "__main__":
    sample_text = """
The Witcher Geralt of Rivia wandered through the dark forests of Kaedwen.
Monsters lurked behind every shadow, yet Geralt’s silver sword gleamed with purpose.
People whispered his name — the White Wolf, the Butcher of Blaviken.
Still, destiny had other plans. The path to Ciri was long, and the Wild Hunt was near.
"""

    # --- Part I: analysis ---
    banner("PART I: ANALYSIS (Text)")
    t1 = Text(sample_text)
    print("Word frequency for 'the':", t1.word_frequency("the"))
    print("Most common word:", t1.most_common_word())
    print("Unique words (first 12):", t1.unique_words()[:12])

    # --- Part II: from_file ---
    banner("PART II: FROM FILE (Text.from_file)")
    base_dir = os.path.dirname(
        __file__) if "__file__" in globals() else os.getcwd()
    file_path = os.path.join(base_dir, "sample.txt")
    try:
        t2 = Text.from_file(file_path)
        print("File loaded:", file_path)
        print("Word frequency for 'Geralt':", t2.word_frequency("Geralt"))
        print("Most common word:", t2.most_common_word())
        print("Unique words (first 12):", t2.unique_words()[:12])
    except Exception as e:
        print("Could not load file:", e)

    # --- Part III: Bonus ---
    banner("BONUS: CLEANING PIPELINE (TextModification)")
    witcher_quote = """
        “The Witcher: Geralt of Rivia” — a monster-hunter for hire, known in every kingdom!
        His silver sword gleamed in moonlight... and his medallion vibrated @ the scent of magic.
        Yet, destiny was cruel — chaos, blood & fire followed him everywhere ©2025 CDPR™.
        Still, he fought for the innocent — and for coin ($), as always...
    """

    t3 = TextModification(witcher_quote)
    before = t3.text
    after = t3.remove_punctuation()
    show_step("remove_punctuation()", before, after)

    t4 = TextModification(witcher_quote)
    before = t4.text
    after = t4.remove_stop_words()
    show_step("remove_stop_words()", before, after)

    t5 = TextModification(witcher_quote)
    before = t5.text
    after = t5.remove_special_characters()
    show_step("remove_special_characters()", before, after)
