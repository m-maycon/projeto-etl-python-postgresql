#%%
import pandas as pd

def main():
    clientes = pd.read_csv("data/raw/clientes.csv")
    produtos = pd.read_csv("data/raw/produtos.csv")
    pedidos = pd.read_csv("data/raw/pedidos.csv")
    itens = pd.read_csv("data/raw/itens_pedido.csv")

    print("CLIENTES")
    print(clientes.head())
    print()

    print("PRODUTOS")
    print(produtos.head())
    print()

    print("PEDIDOS")
    print(pedidos.head())
    print()

    print("ITENS DO PEDIDO")
    print(itens.head())

    print("\n--- INFORMAÇÕES DOS CLIENTES ---")
    print(clientes.info())

    print("\n--- VALORES AUSENTES ---")
    print(clientes.isnull().sum())

    print("\n--- DUPLICIDADES ---")
    print(clientes.duplicated().sum())

    print("\n--- CLIENTE_ID DUPLICADO ---")
    print(clientes["cliente_id"].duplicated().sum())

    print("\n--- ESTADOS ---")
    print(clientes["estado"].value_counts())

    print("\n--- E-MAILS EM MAIÚSCULO ---")
    print(
        clientes[
            clientes["email"].fillna("").str.isupper()
            & clientes["email"].notna()
        ]
    )

    print("\n--- DATAS ---")
    print(clientes["data_cadastro"].head())
    print(clientes["data_cadastro"].dtype)

# INFO PRODUTOS
    print("\n--- INFORMAÇÕES DOS PRODUTOS ---")
    print(produtos.info())

    print("\n--- VALORES AUSENTES PRODUTOS---")
    print(produtos.isnull().sum())

    print("\n---DUPLICIDADES PRODUTOS---")
    print(produtos.duplicated().sum())

#INFO PEDIDOS
    print("\n--- INFORMAÇÕES DOS PEDIDOS ---")
    print(pedidos.info())

    print("\n--- VALORES AUSENTES PEDIDOS ---")
    print(pedidos.isnull().sum())

    print("\n--- STATUS PEDIDOS ---")
    print(pedidos["status"].value_counts())

#INFO ITENS
    print("\n--- INFORMAÇÕES DOS ITENS ---")
    print(itens.info())

    print("\n--- VALORES AUSENTES ITENS ---")
    print(itens.isnull().sum())

#VERIFICA REFERENCIA DE CLIENTES
    clientes_ids = set(clientes["cliente_id"])

    pedidos_clientes_ids = set(pedidos["cliente_id"])

    ids_invalidos = pedidos_clientes_ids - clientes_ids

#VERIFICA REFERENCIA DE PEDIDOS
    print("\n--- CLIENTES DOS PEDIDOS QUE NÃO EXISTEM ---")
    print(ids_invalidos)

    print("\n--- PEDIDOS DOS ITENS QUE NÃO EXISTEM ---")

    pedidos_ids = set(pedidos["pedido_id"])
    itens_pedidos_ids = set(itens["pedido_id"])

    pedidos_invalidos = itens_pedidos_ids - pedidos_ids

    print(pedidos_invalidos)

#VERIFICA REFERENCIA DE PRODUTOS
    print("\n--- PRODUTOS DOS ITENS QUE NÃO EXISTEM ---")

    produtos_ids = set(produtos["produto_id"])
    itens_produtos_ids = set(itens["produto_id"])

    produtos_invalidos = itens_produtos_ids - produtos_ids

    print(produtos_invalidos)

# VERIFICA QUANTIDADE DE ITENS > 0
    print("\n--- QUANTIDADES INVÁLIDAS ---")

    quantidades_invalidas = itens[itens["quantidade"] <= 0]

    print(quantidades_invalidas)

# VERIFICA PREÇOS NEGATIVOS COMO INVALIDOS
    print("\n--- PREÇOS INVÁLIDOS ---")

    precos_invalidos = itens[itens["preco_unitario"] < 0]

    print(precos_invalidos)


    print(pedidos["data_pedido"].dtype)
if __name__ == "__main__":
    main()
# %%
