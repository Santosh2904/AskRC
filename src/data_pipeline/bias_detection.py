import os
import json
import subprocess
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

def pull_dvc_data(dvc_file):
    """
    Pulls data tracked by a .dvc file using the DVC CLI.

    Args:
        dvc_file (str): Path to the .dvc file.
    """
    try:
        print(f"Pulling data for {dvc_file}...")
        subprocess.run(["dvc", "pull", dvc_file], check=True)
        print(f"Data pulled successfully for {dvc_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull data for {dvc_file}: {e}")
        raise

# Path to the .dvc file
dvc_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed.dvc')
)

# Pull data before proceeding
pull_dvc_data(dvc_file)

# Directory where DVC will place the data
base_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed')
)

# Ensure base_dir exists after pulling
if not os.path.exists(base_dir):
    raise NotADirectoryError(f"The base directory provided is not valid: {base_dir}")

def load_json_file(file_path):
    """
    Load JSON content from a file and return a list of content strings.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: List of content strings extracted from the JSON file.

    Raises:
        ValueError: If the JSON structure is unexpected or lacks 'content' keys.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        
        if isinstance(json_data, dict) and 'content' in json_data:
            return [json_data['content']]
        elif isinstance(json_data, list):
            return [item['content'] for item in json_data if 'content' in item]
        
        raise ValueError(f"Unexpected format in {file_path}: expected a list or dict with 'content' field.")

def analyze_sentiment_distribution(text_lines):
    """
    Analyze sentiment distribution and return statistics.

    Args:
        text_lines (list): List of text strings.

    Returns:
        tuple: (polarities, avg_polarity, positive_count, negative_count)
    """
    polarities = [TextBlob(line).sentiment.polarity for line in text_lines]
    avg_polarity = sum(polarities) / len(polarities) if polarities else 0
    positive_count = sum(1 for p in polarities if p > 0)
    negative_count = sum(1 for p in polarities if p < 0)
    
    print(f"Avg Polarity: {avg_polarity:.2f}, Positive: {positive_count}, Negative: {negative_count}")
    return polarities, avg_polarity, positive_count, negative_count

def perform_topic_analysis(text_lines, num_topics=5, num_words=10):
    """
    Perform topic modeling using LDA and display the top words for each topic.

    Args:
        text_lines (list): List of text strings.
        num_topics (int): Number of topics to identify.
        num_words (int): Number of top words to display per topic.

    Returns:
        list: List of top words for each topic.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    text_data = vectorizer.fit_transform(text_lines)
    
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(text_data)
    
    words = vectorizer.get_feature_names_out()
    topics = []
    for i, topic in enumerate(lda.components_):
        top_words = [words[j] for j in topic.argsort()[-num_words:]]
        topics.append(top_words)
        print(f"Topic {i + 1} Keywords: {', '.join(top_words)}")
    
    return topics

def keyword_frequency_analysis(text_lines, num_words=15):
    """
    Perform word frequency analysis on the text data.

    Args:
        text_lines (list): List of text strings.
        num_words (int): Number of top words to display.

    Returns:
        list: List of most common words and their frequencies.
    """
    words = " ".join(text_lines).split()
    counter = Counter(words)
    most_common_words = counter.most_common(num_words)
    
    print("Top Frequent Words:")
    for word, count in most_common_words:
        print(f"{word}: {count}")
    return most_common_words

def slice_data_by_sentiment(text_lines, polarities, num_topics=5, num_words=10):
    """
    Create sentiment-based slices and analyze each slice separately.

    Args:
        text_lines (list): List of text strings.
        polarities (list): List of polarity values for each line.
        num_topics (int): Number of topics to identify in each sentiment slice.
        num_words (int): Number of top words to display per topic/keyword analysis.
    """
    sentiment_slices = {
        'positive': [line for line, polarity in zip(text_lines, polarities) if polarity > 0],
        'negative': [line for line, polarity in zip(text_lines, polarities) if polarity < 0],
    }

    for sentiment, lines in sentiment_slices.items():
        print(f"\n--- Analyzing {sentiment} sentiment slice ---")
        print(f"Number of entries in {sentiment} slice: {len(lines)}")
        
        if lines:
            print(f"\nTopic Analysis for {sentiment} sentiment slice:")
            perform_topic_analysis(lines, num_topics=num_topics, num_words=num_words)
            
            print(f"\nKeyword Frequency Analysis for {sentiment} sentiment slice:")
            keyword_frequency_analysis(lines, num_words=num_words)

def detect_bias_in_directory(base_dir, num_topics=5, num_words=10):
    """
    Run comprehensive bias analysis on all data in the dataset.

    Args:
        base_dir (str): Directory path containing the processed data files.
        num_topics (int): Number of topics to identify in overall and slice-based analysis.
        num_words (int): Number of top words to display per topic/keyword analysis.
    """
    if not os.path.isdir(base_dir):
        raise NotADirectoryError(f"The base directory provided is not valid: {base_dir}")
    
    all_text_lines = []

    for file_name in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file_name)
        if os.path.isfile(file_path):
            print(f"\nLoading file: {file_name}")
            try:
                text_lines = load_json_file(file_path)
                all_text_lines.extend(text_lines)
            except Exception as e:
                print(f"Failed to load {file_name}: {e}")

    if all_text_lines:
        print("\nPerforming Sentiment Analysis on all data:")
        polarities, avg_polarity, positive_count, negative_count = analyze_sentiment_distribution(all_text_lines)
        
        print("\nData Slicing by Sentiment:")
        slice_data_by_sentiment(all_text_lines, polarities, num_topics=num_topics, num_words=num_words)
        
        print("\nOverall Topic Analysis:")
        perform_topic_analysis(all_text_lines, num_topics=num_topics, num_words=num_words)
        
        print("\nOverall Keyword Frequency Analysis:")
        keyword_frequency_analysis(all_text_lines, num_words=num_words)
    else:
        print("No text lines found for analysis.")


if __name__ == "__main__":
    detect_bias_in_directory(base_dir, num_topics=5, num_words=10)
