# tests/test_bias_detection.py

import pytest
from src.evaluation.user_question_bias import check_bias_in_user_question
from src.evaluation.model_response_bias import check_bias_in_model_response

@pytest.mark.parametrize("question, expected_output, expected_message", [
    # Unbiased question
    ("What are the requirements for lab procedures?", 
     "What are the requirements for lab procedures?", 
     None),

    # Biased question with gendered language
    ("Shouldn't he be responsible for this lab task?", 
     None, 
     "We detected some language that might impact the quality of the response. Please consider rephrasing."),

    # Offensive or inappropriate question
    ("Why are certain students always lazy?", 
     None, 
     "We detected some language that might impact the quality of the response. Please consider rephrasing."),
])
def test_check_bias_in_user_question(question, expected_output, expected_message):
    clean_question, message = check_bias_in_user_question(question)
    assert clean_question == expected_output
    assert message == expected_message

@pytest.mark.parametrize("response, expected_clean_response, expected_redaction_message", [
    # Unbiased response
    ("The student needs to complete the experiment within the guidelines.", 
     "The student needs to complete the experiment within the guidelines.", 
     None),

    # Biased response with gendered language
    ("He should be the one handling this project.", 
     "[REDACTED] should be the one handling this project.", 
     "Certain parts of the response were redacted due to potentially inappropriate or biased content."),

    # Response with offensive language
    ("Some people are just lazy in this field.", 
     "Some people are just [REDACTED] in this field.", 
     "Certain parts of the response were redacted due to potentially inappropriate or biased content."),
])
def test_check_bias_in_model_response(response, expected_clean_response, expected_redaction_message):
    clean_response, redaction_message = check_bias_in_model_response(response)
    assert clean_response == expected_clean_response
    assert redaction_message == expected_redaction_message
