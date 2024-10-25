"""
dvc_tracker.py

This module automatically tracks all subdirectories under the 'data/' folder using DVC.
It ensures that changes in the data are versioned and pushed to the remote storage.
"""

import subprocess
import os

# def track_all_data_with_dvc(base_dir='data'):
#     """
#     Automatically track all subdirectories under the base 'data' directory using DVC.
    
    # Args:
    #     base_dir (str): The base directory to search for subdirectories to track (default: 'data').
    # """
    # try:
    #     # Iterate over all subdirectories in the base directory
    #     for dirpath, dirnames, _ in os.walk(base_dir):
    #         for directory in dirnames:
    #             data_dir = os.path.join(dirpath, directory)
                
    #             # Initialize DVC tracking for each subdirectory
    #             if os.path.exists(data_dir):
    #                 # Use DVC to add, commit, and push the data directory
    #                 subprocess.run(['dvc', 'add', data_dir], check=True)
    #                 subprocess.run(['git', 'add', f'{data_dir}.dvc'], check=True)
    #                 subprocess.run(['git', 'commit', '-m', f"Track data: {data_dir}"], check=True)
    #                 subprocess.run(['dvc', 'push'], check=True)
    #                 print(f"Tracked and pushed data for {data_dir} with DVC")
    #             else:
    #                 print(f"Directory {data_dir} does not exist.")
    
    # except subprocess.CalledProcessError as e:
    #     print(f"Error tracking data with DVC: {str(e)}")

def track_all_data_with_dvc(base_dir):
    try:
        for directory in ['raw', 'processed']:
            data_dir = os.path.join(base_dir, directory)
            if os.path.exists(data_dir):
                subprocess.run(['dvc', 'add', data_dir], check=True)
                subprocess.run(['git', 'add', f'{data_dir}.dvc'], check=True)
                subprocess.run(['git', 'commit', '-m', f"Track data: {data_dir}"], check=True)
                subprocess.run(['dvc', 'push'], check=True)
                print(f"Tracked and pushed data for {data_dir} with DVC")
            else:
                print(f"Directory {data_dir} does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Error tracking data with DVC: {str(e)}")