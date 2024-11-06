import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_pipeline.preprocess import clean_text, split_content

def test_clean_text():
    raw_data = "<p>Hello, World! 123</p>"
    clean_text_result = clean_text(raw_data)
    expected_result = "hello world"  # Expected cleaned result without special characters and numbers
    print(f"Raw data: {raw_data}, Cleaned result: {clean_text_result}")
    assert clean_text_result == expected_result, f"Expected '{expected_result}' but got '{clean_text_result}'"

def test_split_content():
    # Test splitting with content exceeding MAX_TERM_SIZE
    long_text = "word " * 10000  # Create a large text to trigger splitting
    parts = split_content(long_text)
    print(f"Number of parts: {len(parts)}")
    assert len(parts) > 1, "Content was not split as expected"
    assert all(len(part.encode('utf-8')) <= 20000 for part in parts), "A part exceeds MAX_TERM_SIZE"

def test_clean_text_edge_cases():
    assert clean_text("") == "", "Failed to handle empty text"
    assert clean_text(None) == "", "Failed to handle None input gracefully"
    print("Edge cases handled correctly in clean_text")
