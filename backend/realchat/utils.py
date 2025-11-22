import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_dataset(path):
    full = os.path.join(BASE_DIR, path)
    print("Loading dataset from:", full)
    return pd.read_excel(full, engine="openpyxl")
