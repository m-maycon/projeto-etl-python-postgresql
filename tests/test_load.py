from unittest.mock import MagicMock

import pytest

from src.load import load_clientes


def test_load_clientes_rollback_em_caso_de_erro():
    conn = MagicMock()

    df = MagicMock()

    conn.cursor.side_effect = Exception("Erro simulado no banco")

    with pytest.raises(Exception, match="Erro simulado no banco"):
        try:
            load_clientes(conn, df)
        except Exception:
            conn.rollback()
            raise

    conn.rollback.assert_called_once()