import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("vader_lexicon")

def analyze_content(text: str, analysis_type: str) -> dict:
    """Analyzes content for various characteristics using NLTK.
    
    Args:
        text (str): The text to analyze
        analysis_type (str): Type of analysis (sentiment, keywords, summary)
        
    Returns:
        dict: Analysis results
    """
    print(f"\n--- Tool Call: analyze_content (type: {analysis_type}) ---")

    try:
        if analysis_type == "sentiment":
            # Initialize sentiment analyzer
            sia = SentimentIntensityAnalyzer()
            sentiment_scores = sia.polarity_scores(text)

            # Determine sentiment label
            compound_score = sentiment_scores["compound"]
            if compound_score >= 0.05:
                label = "positive"
            elif compound_score <= -0.05:
                label = "negative"
            else:
                label = "neutral"

            return {
                "status": "success",
                "analysis": {
                    "score": compound_score,
                    "label": label,
                    "confidence": abs(compound_score),
                    "details": {
                        "positive": sentiment_scores["pos"],
                        "negative": sentiment_scores["neg"],
                        "neutral": sentiment_scores["neu"],
                    },
                },
            }

        elif analysis_type == "keywords":
            # Tokenize and clean text
            words = word_tokenize(text.lower())
            stop_words = set(stopwords.words("english"))
            words = [
                word for word in words if word.isalnum() and word not in stop_words
            ]

            # Get word frequencies
            freq_dist = FreqDist(words)
            top_terms = [word for word, freq in freq_dist.most_common(10)]

            # Calculate term frequencies
            term_frequencies = {word: freq for word, freq in freq_dist.most_common(10)}

            return {
                "status": "success",
                "analysis": {"top_terms": top_terms, "frequency": term_frequencies},
            }

        elif analysis_type == "summary":
            # Split text into sentences
            sentences = sent_tokenize(text)

            # Calculate sentence scores based on word frequency
            word_frequencies = Counter()
            for sentence in sentences:
                words = word_tokenize(sentence.lower())
                word_frequencies.update(words)

            # Score sentences
            sentence_scores = {}
            for i, sentence in enumerate(sentences):
                score = sum(
                    word_frequencies[word.lower()] for word in word_tokenize(sentence)
                )
                sentence_scores[i] = score

            # Get top sentences
            num_sentences = max(
                3, len(sentences) // 3
            )  # Use 1/3 of sentences or at least 3
            top_sentence_indices = sorted(
                sentence_scores, key=sentence_scores.get, reverse=True
            )[:num_sentences]
            top_sentence_indices.sort()  # Sort by original position

            # Create summary
            summary = " ".join(sentences[i] for i in top_sentence_indices)

            return {
                "status": "success",
                "analysis": {
                    "summary": summary,
                    "main_points": [sentences[i] for i in top_sentence_indices],
                    "original_length": len(text.split()),
                    "summary_length": len(summary.split()),
                },
            }

        else:
            return {
                "status": "error",
                "error_message": f"Unsupported analysis type: {analysis_type}",
            }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing content: {str(e)}",
        } 