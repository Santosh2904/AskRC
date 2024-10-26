"""
utils.py

This module provides utility functions used across the project. Specifically, it includes 
a function to calculate the current week based on a predefined start date.
"""

from datetime import datetime

# Define the start date of the project (Week 1 starts on this date)
start_date = datetime.now()  # Adjust this date based on when you want to start tracking weeks

def get_current_week():
    """
    Calculate the current week based on the project start date.

    This function computes the number of weeks that have passed since the start date by dividing 
    the number of days by 7. It adds 1 to represent the current week number.

    Returns:
        int: The current week number (e.g., 1 for the first week, 2 for the second week, etc.).
    """
    current_date = datetime.now()  # Get the current date
    week_number = ((current_date - start_date).days // 7) + 1  # Calculate the current week number
    return week_number
