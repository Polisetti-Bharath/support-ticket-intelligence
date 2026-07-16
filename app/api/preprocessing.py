import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Set up English stopwords with robust offline fallback
try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
        "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
        "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
        "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
        "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
        "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", 
        "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
        "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
        "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
        "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
        "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
    }

# Set up lemmatizer with fallback support
try:
    lemmatizer = WordNetLemmatizer()
    has_lemma = True
except LookupError:
    has_lemma = False


def clean(text: str) -> str:
    """Clean punctuation, lowercase, and strip text."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    """Tokenize clean text string."""
    try:
        return nltk.word_tokenize(text)
    except LookupError:
        return re.findall(r"\b[a-zA-Z]+\b", text)


def preprocess_text(subject: str, body: str) -> str:
    """Preprocess subject and description to return a cleaned string."""
    raw = f"{subject} {body}"
    cleaned = clean(raw)
    tokens = tokenize(cleaned)
    
    # Filter stopwords
    words = [w for w in tokens if w not in stop_words]
    
    # Optional lemmatization
    if has_lemma:
        try:
            words = [lemmatizer.lemmatize(w) for w in words]
        except Exception:
            pass
            
    return " ".join(words)
