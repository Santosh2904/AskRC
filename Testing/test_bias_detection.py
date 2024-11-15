import pytest
from src.evaluation.user_question_bias import check_bias_in_user_question

@pytest.mark.parametrize("question, expected_output, expected_message", [
    # Neutral, unbiased technical question
    ("How do I set up passwordless SSH on a Mac?", 
     "How do I set up passwordless SSH on a Mac?", 
     None),

    # Technical question with a gendered term
    ("How can he set up a virtual environment?", 
     "How can they set up a virtual environment?", 
     None),

    # Biased question with strong negative sentiment
    ("Why are certain students always lazy?", 
     None, 
     "We detected some language that might impact the quality of the response. Please consider rephrasing."),

    # Mild negative sentiment but appropriate technical term
    ("What to do if there is an error during installation?", 
     "What to do if there is an error during installation?", 
     None),

    # Question with strong inappropriate language
    ("The professor is just dumb for suggesting this method.", 
     None, 
     "We detected some language that might impact the quality of the response. Please consider rephrasing."),

    # Question with gendered possessive term
    ("How can her setup be improved?", 
     "How can their setup be improved?", 
     None),

    # Extremely technical question with terms that may trigger sentiment but are correct
    ("What causes connection issues when setting up SSH forwarding?", 
     "What causes connection issues when setting up SSH forwarding?", 
     None),

    # # Another strongly negative but technically correct query (edge case)
    # ("My setup completely failed due to a disastrous error.", 
    #  "My setup completely failed due to a disastrous error.", 
    #  None),
])
def test_check_bias_in_user_question(question, expected_output, expected_message):
    modified_question, message = check_bias_in_user_question(question)
    assert modified_question == expected_output
    assert message == expected_message
