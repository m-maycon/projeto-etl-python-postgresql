import pandas as pd


def transform_clientes(df):
    df = df.copy()

    df["estado"] = df["estado"].str.upper()

    df["email"] = df["email"].str.lower()

    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"])

    return df

def transform_pedidos(df):
    df = df.copy()

    df["data_pedido"] = pd.to_datetime(df["data_pedido"])

    return df

def save_processed_csv(df, file_path):
    """
    Salva um DataFrame como CSV no diretório de dados processados.
    """
    df.to_csv(file_path, index=False)