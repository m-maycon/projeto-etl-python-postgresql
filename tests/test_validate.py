import pandas as pd

from src.validate import (
    validate_clientes,
    validate_produtos,
    validate_pedidos,
    validate_itens_pedido
)


def test_clientes_validos():

    clientes = pd.DataFrame({
        "cliente_id": [1, 2],
        "nome": ["João Silva", "Maria Santos"],
        "email": ["joao@email.com", "maria@email.com"],
        "cidade": ["São Paulo", "Rio de Janeiro"],
        "estado": ["SP", "RJ"],
        "data_cadastro": pd.to_datetime([
            "2025-01-10",
            "2025-01-15"
        ])
    })

    errors = validate_clientes(clientes)

    assert errors == []


def test_cliente_id_duplicado():

    clientes = pd.DataFrame({
        "cliente_id": [1, 1],
        "nome": ["João Silva", "Maria Santos"],
        "email": ["joao@email.com", "maria@email.com"],
        "cidade": ["São Paulo", "Rio de Janeiro"],
        "estado": ["SP", "RJ"],
        "data_cadastro": pd.to_datetime([
            "2025-01-10",
            "2025-01-15"
        ])
    })

    errors = validate_clientes(clientes)

    assert "cliente_id possui valores duplicados." in errors


def test_email_invalido():

    clientes = pd.DataFrame({
        "cliente_id": [1],
        "nome": ["João Silva"],
        "email": ["email-invalido"],
        "cidade": ["São Paulo"],
        "estado": ["SP"],
        "data_cadastro": pd.to_datetime([
            "2025-01-10"
        ])
    })

    errors = validate_clientes(clientes)

    assert "Existem emails inválidos." in errors


def test_produto_com_preco_invalido():

    produtos = pd.DataFrame({
        "produto_id": [1],
        "nome": ["Notebook"],
        "categoria": ["Eletrônicos"],
        "preco": [0],
        "estoque": [10]
    })

    errors = validate_produtos(produtos)

    assert (
        "Existem produtos com preço menor ou igual a zero."
        in errors
    )


def test_produto_com_estoque_negativo():

    produtos = pd.DataFrame({
        "produto_id": [1],
        "nome": ["Notebook"],
        "categoria": ["Eletrônicos"],
        "preco": [4500],
        "estoque": [-1]
    })

    errors = validate_produtos(produtos)

    assert (
        "Existem produtos com estoque negativo."
        in errors
    )


def test_pedido_com_cliente_inexistente():

    clientes = pd.DataFrame({
        "cliente_id": [1],
        "nome": ["João Silva"],
        "email": ["joao@email.com"],
        "cidade": ["São Paulo"],
        "estado": ["SP"],
        "data_cadastro": pd.to_datetime([
            "2025-01-10"
        ])
    })

    pedidos = pd.DataFrame({
        "pedido_id": [1001],
        "cliente_id": [999],
        "data_pedido": pd.to_datetime([
            "2025-05-01"
        ]),
        "status": ["CONCLUIDO"]
    })

    errors = validate_pedidos(
        pedidos,
        clientes
    )

    assert any(
        "clientes inexistentes" in error
        for error in errors
    )


def test_item_com_pedido_inexistente():

    pedidos = pd.DataFrame({
        "pedido_id": [1001],
        "cliente_id": [1],
        "data_pedido": pd.to_datetime([
            "2025-05-01"
        ]),
        "status": ["CONCLUIDO"]
    })

    produtos = pd.DataFrame({
        "produto_id": [1],
        "nome": ["Notebook"],
        "categoria": ["Eletrônicos"],
        "preco": [4500],
        "estoque": [10]
    })

    itens = pd.DataFrame({
        "item_id": [1],
        "pedido_id": [999],
        "produto_id": [1],
        "quantidade": [1],
        "preco_unitario": [4500]
    })

    errors = validate_itens_pedido(
        itens,
        pedidos,
        produtos
    )

    assert any(
        "pedidos inexistentes" in error
        for error in errors
    )


def test_item_com_produto_inexistente():

    pedidos = pd.DataFrame({
        "pedido_id": [1001],
        "cliente_id": [1],
        "data_pedido": pd.to_datetime([
            "2025-05-01"
        ]),
        "status": ["CONCLUIDO"]
    })

    produtos = pd.DataFrame({
        "produto_id": [1],
        "nome": ["Notebook"],
        "categoria": ["Eletrônicos"],
        "preco": [4500],
        "estoque": [10]
    })

    itens = pd.DataFrame({
        "item_id": [1],
        "pedido_id": [1001],
        "produto_id": [999],
        "quantidade": [1],
        "preco_unitario": [4500]
    })

    errors = validate_itens_pedido(
        itens,
        pedidos,
        produtos
    )

    assert any(
        "produtos inexistentes" in error
        for error in errors
    )