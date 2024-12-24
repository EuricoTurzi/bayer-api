import base64
from fastapi import FastAPI
from typing import List
from .database import get_connection
from .models import Resultado

app = FastAPI()

@app.get("/resultados", response_model=List[Resultado])
def get_resultados_sem_imagem():
    """
    Retorna todos os registros da tabela 'resultados' sem a imagem.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            id,
            qr_value,
            max_padroes,
            informacao,
            data_hora,
            NULL AS imagem
        FROM resultados
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Monta a resposta no formato list[Resultado]
    resultados = []
    for row in rows:
        resultado = {
            "id": row[0],
            "qr_value": row[1],
            "max_padroes": row[2],
            "informacao": row[3],
            "data_hora": row[4],
            "imagem": row[5]  # Será None
        }
        resultados.append(resultado)

    cursor.close()
    conn.close()

    return resultados


@app.get("/resultados-com-imagem", response_model=List[Resultado])
def get_resultados_com_imagem():
    """
    Retorna todos os registros da tabela 'resultados' COM a imagem (convertida em base64).
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            id,
            qr_value,
            max_padroes,
            informacao,
            data_hora,
            imagem
        FROM resultados
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    resultados = []
    for row in rows:
        # Converte imagem em base64
        imagem_base64 = None
        if row[5] is not None:
            imagem_base64 = base64.b64encode(row[5]).decode('utf-8')

        resultado = {
            "id": row[0],
            "qr_value": row[1],
            "max_padroes": row[2],
            "informacao": row[3],
            "data_hora": row[4],
            "imagem": imagem_base64
        }
        resultados.append(resultado)

    cursor.close()
    conn.close()

    return resultados
