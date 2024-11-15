import pytest
from src.evaluation.answer_validation import key_concept_match

@pytest.mark.parametrize("answer, context, expected", [
    # Exact match of concept in context
    (
        "To set up passwordless SSH on a Mac, you need to generate SSH keys and add them to the authorized_keys file.",
        "Passwordless SSH On A Mac: Set up passwordless SSH to ensure GUI applications run without issues. Ensure your keys are added to the authorized_keys file in ~/.ssh. This needs to be done each time SSH keys are regenerated.",
        True
    ),
    
    # Partially overlapping terms with context
    (
        "Use the slurm command for handling job dependencies in cluster computing.",
        "Our HPC cluster uses the Slurm Workload Manager. Jobs are queued and scheduled based on resource availability and priority factors like fairshare and queue wait time.",
        False  # Should not pass as a match due to insufficiently close context
    ),
    
    # Overlapping technical concepts but incorrect context
    (
        "To run parallel jobs, submit a job array using sbatch.",
        "The queuing system uses a fair-share policy to manage resources over time. Smaller jobs have higher priority, and jobs waiting longer in the queue gain priority.",
        False  # Should not pass due to lack of specific detail about job arrays
    ),
    
    # Correct context regarding job scheduling in HPC
    (
        "The fair-share policy ensures balanced resource allocation, prioritizing jobs based on fairshare, job size, and queue wait time.",
        "Scheduling Policies: Our cluster uses fair-share scheduling, prioritizing jobs based on fairshare, job size, and queue wait time to balance resource allocation.",
        True
    ),
    
    # General answer about HPC parallel jobs, should fail on specificity
    (
        "To execute parallel jobs, manage your resources with job arrays.",
        "In HPC, job arrays are beneficial for managing similar jobs. This setup allows researchers to perform tasks efficiently with different inputs and configurations.",
        False
    ),
    
    # Unrelated answer about software not related to context
    (
        "Use TensorFlow for GPU acceleration in deep learning tasks.",
        "The queuing system in our HPC environment uses Slurm to schedule jobs. It balances CPU, memory, and GPU allocation based on job priority and fair-share policies.",
        False
    ),
])
def test_key_concept_match(answer, context, expected):
    result = key_concept_match(answer, context)
    assert result == expected, f"Expected {expected} for answer '{answer}' with context '{context}', but got {result}"
