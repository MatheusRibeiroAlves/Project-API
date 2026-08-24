import os
import pytest
import pymysql

MYSQL_HOST = os.environ.get("MYSQL_HOST")

pytestmark = pytest.mark.skipif(
    MYSQL_HOST is None,
    reason="MySQL não disponível localmente — este teste só roda no CI"
)


def get_connection(database=None):
    return pymysql.connect(
        host=MYSQL_HOST,
        user="root",
        password="test_password",
        database=database,
        port=3306,
    )


def test_mysql_conexao():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    conn.close()
    assert result[0] == 1


def test_mysql_criar_tabela_e_inserir():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test_db")
    conn.close()

    conn = get_connection(database="test_db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS imoveis (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            cidade VARCHAR(100),
            estado CHAR(2),
            valor  DECIMAL(12,2)
        )
    """)
    cursor.execute(
        "INSERT INTO imoveis (titulo, cidade, estado, valor) VALUES (%s, %s, %s, %s)",
        ("Apartamento Teste", "São Paulo", "SP", 500000.00),
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM imoveis")
    count = cursor.fetchone()[0]
    conn.close()

    assert count >= 1


def test_mysql_buscar_imovel():
    conn = get_connection(database="test_db")
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, cidade FROM imoveis WHERE estado = %s", ("SP",))
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) >= 1
    assert rows[0][1] == "São Paulo"
