import pytest
import sys
import os
from unittest.mock import patch

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Mock the azure_uploader module before importing preprocess
mock_azure_uploader = patch('src.data_pipeline.azure_uploader.upload_to_blob').start()

# Now import the functions to test
from src.data_pipeline.preprocess import clean_text, split_content, MAX_TERM_SIZE

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    yield
    # Teardown
    patch.stopall()

def test_clean_text():
    test_cases = [
        ("<p>Hello, World! 123</p>", "hello world"),
        ("Test@123", "test"),
        ("<div>Multiple Words Here!</div>", "multiple words"),
        ("Numbers123 and Spaces   Test", "numbers spaces test"),
    ]
    
    for input_text, expected in test_cases:
        result = clean_text(input_text)
        print(f"Input: {input_text}, Result: {result}, Expected: {expected}")
        assert result == expected, f"Expected '{expected}' but got '{result}'"

def test_split_content():
    # Create a string that will definitely exceed MAX_TERM_SIZE
    # Using a simple repeating pattern
    base_word = "test" * 25  # 100 characters
    # Create a string that's definitely larger than MAX_TERM_SIZE
    test_text = f"{base_word} " * 300  # Should create multiple chunks
    
    parts = split_content(test_text)
    
    print(f"MAX_TERM_SIZE: {MAX_TERM_SIZE}")
    print(f"Number of parts: {len(parts)}")
    
    # Verify we got multiple parts
    assert len(parts) > 1, "Text should have been split into multiple parts"
    
    # Verify each part is within size limit
    for i, part in enumerate(parts):
        part_size = len(part.encode('utf-8'))
        print(f"Part {i} size: {part_size}")
        assert part_size <= MAX_TERM_SIZE, (
            f"Part {i} exceeds MAX_TERM_SIZE: {part_size} > {MAX_TERM_SIZE}"
        )

def test_clean_text_edge_cases():
    assert clean_text("") == "", "Failed to handle empty text"
    assert clean_text(None) == "", "Failed to handle None input gracefully"
    print("Edge cases handled correctly in clean_text")

def test_split_content_edge_cases():
    # Test empty string
    assert split_content("") == [], "Empty string should return empty list"
    
    # Test single word
    single_word = "test"
    assert split_content(single_word) == [single_word], "Single word should return single part"
    
    # Test string smaller than MAX_TERM_SIZE
    small_text = "This is a small text"
    assert split_content(small_text) == [small_text], "Small text should not be split"
    
    # Test very long single word
    very_long_word = "a" * (MAX_TERM_SIZE + 1000)
    parts = split_content(very_long_word)
    assert all(len(part.encode('utf-8')) <= MAX_TERM_SIZE for part in parts), (
        "Even long words should be split into acceptable sizes"
    )