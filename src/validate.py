import pandas as pd


def validate_clientes(clientes):
    """
    Valida a qualidade e integridade dos dados de clientes.
    """

    errors = []

    # cliente_id
    if clientes["cliente_id"].isnull().any():
        errors.append(
            "cliente_id possui valores nulos."
        )

    if clientes["cliente_id"].duplicated().any():
        errors.append(
            "cliente_id possui valores duplicados."
        )

    # nome
    if clientes["nome"].isnull().any():
        errors.append(
            "nome possui valores nulos."
        )

    # email
    email_valido = clientes["email"].isna() | (
        clientes["email"].str.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            na=False
        )
    )

    if not email_valido.all():
        errors.append(
            "Existem emails inválidos."
        )

    # estado
    estado_valido = clientes["estado"].str.len().eq(2)

    if not estado_valido.all():
        errors.append(
            "Existem estados com formato inválido."
        )

    # data_cadastro
    if clientes["data_cadastro"].isnull().any():
        errors.append(
            "data_cadastro possui valores inválidos."
        )

    return errors


def validate_produtos(produtos):
    """
    Valida a qualidade e integridade dos dados de produtos.
    """

    errors = []

    # produto_id
    if produtos["produto_id"].isnull().any():
        errors.append(
            "produto_id possui valores nulos."
        )

    if produtos["produto_id"].duplicated().any():
        errors.append(
            "produto_id possui valores duplicados."
        )

    # nome
    if produtos["nome"].isnull().any():
        errors.append(
            "nome possui valores nulos."
        )

    # preço
    if (produtos["preco"] <= 0).any():
        errors.append(
            "Existem produtos com preço menor ou igual a zero."
        )

    # estoque
    if (produtos["estoque"] < 0).any():
        errors.append(
            "Existem produtos com estoque negativo."
        )

    return errors


def validate_pedidos(pedidos, clientes):
    """
    Valida a qualidade e integridade dos dados de pedidos.
    """

    errors = []

    # pedido_id
    if pedidos["pedido_id"].isnull().any():
        errors.append(
            "pedido_id possui valores nulos."
        )

    if pedidos["pedido_id"].duplicated().any():
        errors.append(
            "pedido_id possui valores duplicados."
        )

    # cliente_id
    clientes_ids = set(clientes["cliente_id"])
    pedidos_clientes_ids = set(pedidos["cliente_id"])

    ids_invalidos = pedidos_clientes_ids - clientes_ids

    if ids_invalidos:
        errors.append(
            f"Existem pedidos associados a clientes inexistentes: "
            f"{ids_invalidos}"
        )

    # status
    status_validos = {
        "CONCLUIDO",
        "CANCELADO",
        "PENDENTE"
    }

    status_invalidos = set(pedidos["status"]) - status_validos

    if status_invalidos:
        errors.append(
            f"Existem status inválidos: {status_invalidos}"
        )

    # data_pedido
    if pedidos["data_pedido"].isnull().any():
        errors.append(
            "data_pedido possui valores inválidos."
        )

    return errors


def validate_itens_pedido(itens_pedido, pedidos, produtos):
    """
    Valida a qualidade e integridade dos itens dos pedidos.
    """

    errors = []

    # item_id
    if itens_pedido["item_id"].isnull().any():
        errors.append(
            "item_id possui valores nulos."
        )

    if itens_pedido["item_id"].duplicated().any():
        errors.append(
            "item_id possui valores duplicados."
        )

    # quantidade
    if (itens_pedido["quantidade"] <= 0).any():
        errors.append(
            "Existem itens com quantidade menor ou igual a zero."
        )

    # preço unitário
    if (itens_pedido["preco_unitario"] <= 0).any():
        errors.append(
            "Existem itens com preço unitário menor ou igual a zero."
        )

    # pedido_id
    pedidos_ids = set(pedidos["pedido_id"])
    itens_pedidos_ids = set(itens_pedido["pedido_id"])

    pedidos_invalidos = itens_pedidos_ids - pedidos_ids

    if pedidos_invalidos:
        errors.append(
            f"Existem itens associados a pedidos inexistentes: "
            f"{pedidos_invalidos}"
        )

    # produto_id
    produtos_ids = set(produtos["produto_id"])
    itens_produtos_ids = set(itens_pedido["produto_id"])

    produtos_invalidos = itens_produtos_ids - produtos_ids

    if produtos_invalidos:
        errors.append(
            f"Existem itens associados a produtos inexistentes: "
            f"{produtos_invalidos}"
        )

    return errors


def validate_all(clientes, produtos, pedidos, itens_pedido):
    """
    Executa todas as validações do pipeline.
    """

    validation_errors = {
        "clientes": validate_clientes(clientes),
        "produtos": validate_produtos(produtos),
        "pedidos": validate_pedidos(
            pedidos,
            clientes
        ),
        "itens_pedido": validate_itens_pedido(
            itens_pedido,
            pedidos,
            produtos
        )
    }

    total_errors = sum(
        len(errors)
        for errors in validation_errors.values()
    )

    if total_errors > 0:

        print("\n--- DATA QUALITY ---")

        for table, errors in validation_errors.items():

            if errors:

                print(f"\n❌ {table}")

                for error in errors:
                    print(f"   - {error}")

        raise ValueError(
            f"Pipeline interrompido: "
            f"{total_errors} erro(s) de qualidade encontrados."
        )

    print("\n--- DATA QUALITY ---")
    print("✅ Todas as validações passaram.")
