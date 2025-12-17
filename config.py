# config.py
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_data_path(filename):
    return os.path.join(PROJECT_ROOT, 'data', filename)

def get_model_path(filename):
    return os.path.join(PROJECT_ROOT, 'models', filename)
