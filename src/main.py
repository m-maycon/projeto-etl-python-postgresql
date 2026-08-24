from extract import extract_csv
from validate import (
    validate_not_null,
    validate_unique,
    validate_foreign_key,
    validate_uppercase,
    validate_lowercase,
    validate_datetime,
)
from transform import transform_clientes, transform_pedidos, save_processed_csv

def main():
    clientes = extract_csv("data/raw/clientes.csv")
    produtos = extract_csv("data/raw/produtos.csv")
    pedidos = extract_csv("data/raw/pedidos.csv")
    itens = extract_csv("data/raw/itens_pedido.csv")

    clientes = transform_clientes(clientes)
    pedidos = transform_pedidos(pedidos)

    produtos_processados = produtos.copy()
    itens_processados = itens.copy()

    print("Clientes:", len(clientes))
    print("Produtos:", len(produtos))
    print("Pedidos:", len(pedidos))
    print("Itens:", len(itens))

    print("Cliente ID válido:",validate_not_null(clientes, "cliente_id"))

    print("Email válido:",validate_not_null(clientes, "email"))

    print("Cliente ID único:",validate_unique(clientes, "cliente_id"))

    print("Pedidos -> Clientes:",validate_foreign_key(
        pedidos,
        "cliente_id",
        clientes,
        "cliente_id"
    )
    )

    print("Itens -> Pedidos:",validate_foreign_key(
        itens,
        "pedido_id",
        pedidos,
        "pedido_id"
    )
    )

    print("Itens -> Produtos:",validate_foreign_key(
        itens,
        "produto_id",
        produtos,
        "produto_id"
    )
    )

    print("\n--- CLIENTES TRANSFORMADOS ---")
    print(clientes.head())
    print(clientes.dtypes)

    print("\n--- PEDIDOS TRANSFORMADOS ---")
    print(pedidos.head())
    print(pedidos.dtypes)

    print("\n--- VALIDAÇÃO PÓS-TRANSFORMAÇÃO ---")

    print("Estado em uppercase:", validate_uppercase(clientes, "estado"))

    print("Email em lowercase:",validate_lowercase(clientes, "email"))

    print("Data de cadastro válida:",validate_datetime(clientes, "data_cadastro"))

    print("Data do pedido válida:",validate_datetime(pedidos, "data_pedido"))

    save_processed_csv(clientes, "data/processed/clientes.csv")

    save_processed_csv(produtos_processados,"data/processed/produtos.csv")

    save_processed_csv(pedidos,"data/processed/pedidos.csv")

    save_processed_csv(itens_processados,"data/processed/itens_pedido.csv")
if __name__ == "__main__":
    main()
