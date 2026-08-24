import pandas as pd


def extract_csv(file_path):
    """
    Lê um arquivo CSV e retorna um DataFrame.
    """
    return pd.read_csv(file_path)