import pandas as pd

def validate_not_null(df, column):
    """
    Verifica se uma coluna possui valores nulos.

    Retorna True quando não existem valores nulos.
    """
    return df[column].notna().all()


def validate_unique(df, column):
    """
    Verifica se os valores de uma coluna são únicos.
    """
    return df[column].is_unique

def validate_foreign_key(child_df, child_column, parent_df, parent_column):
    """
    Verifica se todos os valores da chave estrangeira
    existem na tabela pai.
    """
    child_values = set(child_df[child_column])
    parent_values = set(parent_df[parent_column])

    invalid_values = child_values - parent_values

    return len(invalid_values) == 0

def validate_uppercase(df, column):
    """
    Verifica se todos os valores preenchidos de uma coluna
    estão em letras maiúsculas.
    """
    values = df[column].dropna().astype(str)

    return values.eq(values.str.upper()).all()

def validate_lowercase(df, column):
    """
    Verifica se todos os valores preenchidos de uma coluna
    estão em letras minúsculas.
    """
    values = df[column].dropna().astype(str)

    return values.eq(values.str.lower()).all()

def validate_datetime(df, column):
    """
    Verifica se uma coluna possui valores de data válidos.
    """
    return pd.api.types.is_datetime64_any_dtype(df[column])