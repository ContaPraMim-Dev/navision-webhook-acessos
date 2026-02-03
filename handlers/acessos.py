import json
import re
import requests


def _validar_uuid(valor: str) -> bool:
    """Valida se o valor é um UUID válido."""
    padrao = re.compile(
        r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    )
    return bool(padrao.match(valor))


def _validar_data_simples(valor: str) -> bool:
    """Valida se a data está no formato yyyy-mm-dd."""
    padrao = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(padrao.match(valor))


def _validar_data_iso(valor: str) -> bool:
    """Valida se a data está no formato ISO 8601 com timezone (ex: 2028-11-25T23:59:59-03:00)."""
    padrao = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$')
    return bool(padrao.match(valor))


def _validar_body_acessos(body: dict) -> tuple[bool, str]:
    """
    Valida o body do webhook de acessos.
    Retorna (True, "") se válido, ou (False, mensagem_erro) se inválido.
    """
    # Validar event_id (UUID válido)
    event_id = body.get("event_id")
    if not event_id or not isinstance(event_id, str) or not _validar_uuid(event_id):
        return False, "event_id deve ser um UUID válido."

    data = body.get("data")
    if not data or not isinstance(data, dict):
        return False, "data deve ser um objeto."

    # Validar isps_code (string)
    isps_code = data.get("isps_code")
    if not isinstance(isps_code, str):
        return False, "isps_code deve ser uma string."

    # Validar nome_completo (string)
    nome_completo = data.get("nome_completo")
    if not isinstance(nome_completo, str):
        return False, "nome_completo deve ser uma string."

    # Validar tipo_acesso (VERMELHO ou VERDE)
    tipo_acesso = data.get("tipo_acesso")
    if tipo_acesso not in ("VERMELHO", "VERDE"):
        return False, "tipo_acesso deve ser VERMELHO ou VERDE."

    # Validar motivacao_inicio (formato yyyy-mm-dd)
    motivacao_inicio = data.get("motivacao_inicio")
    if not isinstance(motivacao_inicio, str) or not _validar_data_simples(motivacao_inicio):
        return False, "motivacao_inicio deve estar no formato yyyy-mm-dd."

    # Validar motivacao_fim (formato ISO 8601 com timezone)
    motivacao_fim = data.get("motivacao_fim")
    if not isinstance(motivacao_fim, str) or not _validar_data_iso(motivacao_fim):
        return False, "motivacao_fim deve estar no formato ISO 8601 (ex: 2028-11-25T23:59:59-03:00)."

    # Validar empresa (string)
    empresa = data.get("empresa")
    if not isinstance(empresa, str):
        return False, "empresa deve ser uma string."

    # Validar id_foto (inteiro)
    id_foto = data.get("id_foto")
    if not isinstance(id_foto, int):
        return False, "id_foto deve ser um inteiro."

    # Validar gate (inteiro)
    gate = data.get("gate")
    if not isinstance(gate, int):
        return False, "gate deve ser um inteiro."

    return True, ""


def _enviar_para_navision(data: dict, api_key: str) -> int | None:
    """
    Envia os dados para a API do Navision.
    Retorna o status code da resposta ou None em caso de erro de conexão.
    """
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
    }

    max_tentativas = 3

    for tentativa in range(max_tentativas):
        try:
            response = requests.post(
                "https://xkit-1dzl-gome.n7c.xano.io/api:yXFPZvLr/webhook_acessos",
                json=data,
                headers=headers,
            )
            print(f"Status Code do Navision: {response.text}")
            return int(response.text)
        except Exception as e:
            print(f"Tentativa {tentativa + 1} de {max_tentativas} falhou.")
            print(f"Erro ao enviar para Navision: {e}")
            if tentativa == max_tentativas - 1:
                return None
    return None


def handler_acessos(body: dict, api_key: str) -> dict:
    """
    Handler para eventos do tipo 'acessos'.
    Valida o body e envia para o Navision.
    """
    # Validação do body (erro 400)
    valido, mensagem_erro = _validar_body_acessos(body)
    if not valido:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "erro",
                "mensagem": f"Erro de requisição — {mensagem_erro}"
            })
        }

    # Montar payload para o Xano (tudo no mesmo nível)
    payload = {"event_id": body.get("event_id"), **body.get("data")}
    status_code = _enviar_para_navision(payload, api_key)

    if status_code is None or status_code == 500:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "erro",
                "mensagem": "Erro interno do servidor."
            })
        }

    if status_code == 401:
        return {
            "statusCode": 401,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "erro",
                "mensagem": "Chave de API não autorizada."
            })
        }

    if status_code == 409:
        return {
            "statusCode": 409,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "status": "erro",
                "mensagem": "Conflito — evento já registrado."
            })
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "status": "sucesso"
        })
    }
