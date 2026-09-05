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

def transform_itens_pedido(df):
    """
    Realiza as transformações dos itens dos pedidos.
    """

    df = df.copy()

    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    return df