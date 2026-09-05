import os

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv


load_dotenv()

def create_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return conn

def load_clientes(conn, df):
    """
    Insere os clientes no PostgreSQL
    """

    query = """
        INSERT INTO clientes (
            cliente_id,
            nome,
            email,
            cidade,
            estado,
            data_cadastro
        )
        VALUES %s
        ON CONFLICT (cliente_id)
        DO UPDATE SET
            nome = EXCLUDED.nome,
            email = EXCLUDED.email,
            cidade = EXCLUDED.cidade,
            estado = EXCLUDED.estado,
            data_cadastro = EXCLUDED.data_cadastro;
"""
    values = [
        tuple(row)
        for row in df[
            [
                "cliente_id",
                "nome",
                "email",
                "cidade",
                "estado",
                "data_cadastro"
            ]
        ].itertuples(index=False, name=None)
    ]

    with conn.cursor() as cursor:
        execute_values(cursor, query, values)

def load_produtos(conn, df):
    """
    Insere os produtos no PostgreSQL.
    """

    query = """
        INSERT INTO produtos (
            produto_id,
            nome,
            categoria,
            preco,
            estoque
        )
        VALUES %s
        ON CONFLICT (produto_id)
        DO UPDATE SET
            nome = EXCLUDED.nome,
            categoria = EXCLUDED.categoria,
            preco = EXCLUDED.preco,
            estoque = EXCLUDED.estoque;
    """

    values = [
        tuple(row)
        for row in df[
            [
                "produto_id",
                "nome",
                "categoria",
                "preco",
                "estoque"
            ]
        ].itertuples(index=False, name=None)
    ]

    with conn.cursor() as cursor:
        execute_values(cursor, query, values)

def load_pedidos(conn, df):
    """
    Insere ou atualiza pedidos no PostgreSQL.
    """

    query = """
        INSERT INTO pedidos (
            pedido_id,
            cliente_id,
            data_pedido,
            status
        )
        VALUES %s
        ON CONFLICT (pedido_id)
        DO UPDATE SET
            cliente_id = EXCLUDED.cliente_id,
            data_pedido = EXCLUDED.data_pedido,
            status = EXCLUDED.status;
    """

    values = [
        tuple(row)
        for row in df[
            [
                "pedido_id",
                "cliente_id",
                "data_pedido",
                "status"
            ]
        ].itertuples(index=False, name=None)
    ]

    with conn.cursor() as cursor:
        execute_values(cursor, query, values)


def load_itens_pedido(conn, df):
    """
    Insere ou atualiza itens dos pedidos no PostgreSQL.
    """

    query = """
        INSERT INTO itens_pedido (
            item_id,
            pedido_id,
            produto_id,
            quantidade,
            preco_unitario
        )
        VALUES %s
        ON CONFLICT (item_id)
        DO UPDATE SET
            pedido_id = EXCLUDED.pedido_id,
            produto_id = EXCLUDED.produto_id,
            quantidade = EXCLUDED.quantidade,
            preco_unitario = EXCLUDED.preco_unitario;
    """

    values = [
        tuple(row)
        for row in df[
            [
                "item_id",
                "pedido_id",
                "produto_id",
                "quantidade",
                "preco_unitario"
            ]
        ].itertuples(index=False, name=None)
    ]

    with conn.cursor() as cursor:
        execute_values(cursor, query, values)
