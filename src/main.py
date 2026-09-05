from src.extract import extract_csv

from src.transform import (
    transform_clientes,
    transform_pedidos,
    transform_itens_pedido
)

from src.validate import validate_all

from src.load import (
    create_connection,
    load_clientes,
    load_produtos,
    load_pedidos,
    load_itens_pedido
)


def main():

    # =====================
    # EXTRACT
    # =====================

    clientes = extract_csv("data/raw/clientes.csv")
    produtos = extract_csv("data/raw/produtos.csv")
    pedidos = extract_csv("data/raw/pedidos.csv")
    itens_pedido = extract_csv("data/raw/itens_pedido.csv")


    # =====================
    # TRANSFORM
    # =====================

    clientes = transform_clientes(clientes)

    pedidos = transform_pedidos(pedidos)

    itens_pedido = transform_itens_pedido(itens_pedido)


    # =====================
    # VALIDATE
    # =====================

    validate_all(
        clientes,
        produtos,
        pedidos,
        itens_pedido
    )


    # =====================
    # LOAD
    # =====================

    conn = create_connection()

    try:

        load_clientes(conn, clientes)

        load_produtos(conn, produtos)

        load_pedidos(conn, pedidos)

        load_itens_pedido(conn, itens_pedido)

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    finally:

        conn.close()


    print("\nPipeline ETL executado com sucesso!")


if __name__ == "__main__":
    main()
