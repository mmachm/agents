import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from datetime import datetime
from typing import Dict, List

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")

def summarize_findings(data: List[Dict], format: str) -> dict:
    """Summarizes research findings using advanced text analysis.
    
    Args:
        data (List[Dict]): List of research findings, each containing:
            - 'content': Text content to analyze
            - 'source': Source of the content
            - 'metadata': Additional metadata
        format (str): Summary format ('brief', 'detailed', 'structured')
        
    Returns:
        dict: Summary of findings
    """
    print(f"\n--- Tool Call: summarize_findings (format: {format}) ---")

    try:
        # Combine all content
        all_content = " ".join(item.get("content", "") for item in data)

        # Tokenize and clean text
        sentences = sent_tokenize(all_content)
        words = word_tokenize(all_content.lower())
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word.isalnum() and word not in stop_words]

        # Calculate word frequencies
        word_frequencies = Counter(words)

        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = sum(
                word_frequencies[word.lower()] for word in word_tokenize(sentence)
            )
            sentence_scores[i] = score

        # Get top sentences
        num_sentences = max(3, len(sentences) // 3)
        top_sentence_indices = sorted(
            sentence_scores, key=sentence_scores.get, reverse=True
        )[:num_sentences]
        top_sentence_indices.sort()

        # Create summaries
        brief_summary = " ".join(sentences[i] for i in top_sentence_indices[:2])
        detailed_summary = " ".join(sentences[i] for i in top_sentence_indices)

        # Create structured summary
        structured_summary = {
            "key_findings": [sentences[i] for i in top_sentence_indices],
            "top_keywords": [word for word, _ in word_frequencies.most_common(5)],
            "sources": list(set(item.get("source", "Unknown") for item in data)),
            "metadata": {
                "total_sources": len(data),
                "total_sentences": len(sentences),
                "summary_length": len(detailed_summary.split()),
            },
        }

        # Return appropriate format
        if format == "brief":
            return {
                "status": "success",
                "summary": brief_summary,
                "format": format,
                "timestamp": datetime.now().isoformat(),
            }
        elif format == "detailed":
            return {
                "status": "success",
                "summary": detailed_summary,
                "format": format,
                "timestamp": datetime.now().isoformat(),
            }
        elif format == "structured":
            return {
                "status": "success",
                "summary": structured_summary,
                "format": format,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            return {"status": "error", "error_message": f"Unsupported format: {format}"}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error summarizing findings: {str(e)}",
        } 